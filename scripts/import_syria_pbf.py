#!/usr/bin/env python3
"""Stream the Syria OSM PBF into a compact nationwide searchable object index.

The original PBF remains the geometry/source snapshot. SQLite stores searchable
object records, representative coordinates and bounding boxes.
"""
import sqlite3
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools/python"))
import osmium

PBF=ROOT/"data/national/syria-latest.osm.pbf"
TARGET=ROOT/"data/national/syria_catalog.sqlite"

SCHEMA="""
PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=MEMORY;
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE roads(osm_id INTEGER PRIMARY KEY,technical_code TEXT UNIQUE NOT NULL,name_ar TEXT,name_en TEXT,name TEXT,
 highway TEXT,ref TEXT,lon REAL,lat REAL,min_lon REAL,min_lat REAL,max_lon REAL,max_lat REAL,source_status TEXT NOT NULL);
CREATE TABLE buildings(osm_id INTEGER PRIMARY KEY,technical_code TEXT UNIQUE NOT NULL,building_type TEXT,
 lon REAL,lat REAL,min_lon REAL,min_lat REAL,max_lon REAL,max_lat REAL,source_status TEXT NOT NULL);
CREATE TABLE places(osm_id INTEGER PRIMARY KEY,technical_code TEXT UNIQUE NOT NULL,name_ar TEXT,name_en TEXT,name TEXT,
 place_type TEXT,population TEXT,lon REAL,lat REAL,source_status TEXT NOT NULL);
"""

class Importer(osmium.SimpleHandler):
    def __init__(self,conn):
        super().__init__();self.conn=conn;self.roads=0;self.buildings=0;self.places=0
    def node(self,n):
        if "place" not in n.tags or not n.location.valid():return
        self.conn.execute("INSERT OR REPLACE INTO places VALUES(?,?,?,?,?,?,?,?,?,?)",
          (n.id,f"SY-OSM-PLACE-{n.id}",n.tags.get("name:ar"),n.tags.get("name:en"),n.tags.get("name"),
           n.tags.get("place"),n.tags.get("population"),n.location.lon,n.location.lat,"OPEN_DATA_UNVERIFIED"))
        self.places+=1
    def way(self,w):
        is_road="highway" in w.tags;is_building="building" in w.tags
        if not (is_road or is_building):return
        pts=[(x.lon,x.lat) for x in w.nodes if x.location.valid()]
        if len(pts)<2:return
        xs=[p[0] for p in pts];ys=[p[1] for p in pts];lon=sum(xs)/len(xs);lat=sum(ys)/len(ys)
        bounds=(min(xs),min(ys),max(xs),max(ys))
        if is_road:
            self.conn.execute("INSERT OR REPLACE INTO roads VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (w.id,f"SY-OSM-ROAD-{w.id}",w.tags.get("name:ar"),w.tags.get("name:en"),w.tags.get("name"),
               w.tags.get("highway"),w.tags.get("ref"),lon,lat,*bounds,"OPEN_DATA_UNVERIFIED"))
            self.roads+=1
        if is_building:
            self.conn.execute("INSERT OR REPLACE INTO buildings VALUES(?,?,?,?,?,?,?,?,?,?)",
              (w.id,f"SY-OSM-BLD-{w.id}",w.tags.get("building"),lon,lat,*bounds,"OPEN_DATA_UNVERIFIED"))
            self.buildings+=1

def main():
    if not PBF.exists():raise SystemExit(f"Missing {PBF}")
    if TARGET.exists():TARGET.unlink()
    conn=sqlite3.connect(TARGET);conn.executescript(SCHEMA)
    started=time.time();handler=Importer(conn);handler.apply_file(str(PBF),locations=True)
    conn.execute("CREATE INDEX roads_name_idx ON roads(name)")
    conn.execute("CREATE INDEX roads_name_ar_idx ON roads(name_ar)")
    conn.execute("CREATE INDEX roads_name_en_idx ON roads(name_en)")
    conn.execute("CREATE INDEX buildings_code_idx ON buildings(technical_code)")
    conn.execute("CREATE INDEX places_name_idx ON places(name)")
    for key,value in {"source":"Geofabrik / OpenStreetMap contributors","license":"ODbL 1.0",
                      "scope":"Syrian Arab Republic","imported_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
                      "roads":handler.roads,"buildings":handler.buildings,"places":handler.places}.items():
        conn.execute("INSERT INTO metadata VALUES(?,?)",(key,str(value)))
    conn.commit();conn.execute("VACUUM");conn.close()
    print(f"roads={handler.roads} buildings={handler.buildings} places={handler.places} seconds={time.time()-started:.1f}")

if __name__=="__main__":main()
