#!/usr/bin/env python3
"""Extract an unverified Al-Zabadani pilot from the local Syria OSM snapshot."""
import json
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools/python"))

PBF=ROOT/"data/national/syria-latest.osm.pbf"
OVERPASS=ROOT/"data/import/zabadani_osm.json"
ROADS=ROOT/"data/zabadani_rif_dimashq_roads.geojson"
BUILDINGS=ROOT/"data/zabadani_rif_dimashq_buildings.geojson"
BOUNDS=(36.080,33.705,36.120,33.740)

class Extractor:
    def __init__(self):
        self.roads=[];self.buildings=[]
    def way(self,way):
        if "highway" not in way.tags and "building" not in way.tags:return
        points=[(node.lon,node.lat) for node in way.nodes if node.location.valid()]
        if len(points)<2:return
        lon=sum(p[0] for p in points)/len(points);lat=sum(p[1] for p in points)/len(points)
        west,south,east,north=BOUNDS
        if not (west<=lon<=east and south<=lat<=north):return
        tags=way.tags
        if "highway" in tags:
            self.roads.append({"type":"Feature","id":f"osm-way-{way.id}",
              "geometry":{"type":"LineString","coordinates":points},
              "properties":{"technical_code":f"SY-RD-ZA-ZAB-RD-OSM-{way.id}","osm_way_id":way.id,
                "name_ar":tags.get("name:ar") or tags.get("name"),"name_en":tags.get("name:en"),
                "highway":tags.get("highway"),"surface":tags.get("surface"),
                "source":"OpenStreetMap contributors","quality_level":"D",
                "official_status":"IMPORTED_UNVERIFIED"}})
        if "building" in tags and len(points)>=3:
            if points[0]!=points[-1]:points.append(points[0])
            self.buildings.append({"type":"Feature","id":f"osm-building-{way.id}",
              "geometry":{"type":"Polygon","coordinates":[points]},
              "properties":{"technical_code":f"SY-RD-ZA-ZAB-BLD-OSM-{way.id}","osm_way_id":way.id,
                "building_type":tags.get("building","yes"),"centroid":[lon,lat],
                "quality_level":"D","official_status":"IMPORTED_UNVERIFIED",
                "source":"OpenStreetMap contributors"}})

def main():
    handler=Extractor()
    if OVERPASS.exists():
        raw=json.loads(OVERPASS.read_text(encoding="utf-8"))
        for item in raw.get("elements",[]):
            if item.get("type")!="way":continue
            points=[(point["lon"],point["lat"]) for point in item.get("geometry",[])]
            if len(points)<2:continue
            tags=item.get("tags",{});way_id=item["id"]
            lon=sum(p[0] for p in points)/len(points);lat=sum(p[1] for p in points)/len(points)
            if "highway" in tags:
                handler.roads.append({"type":"Feature","id":f"osm-way-{way_id}",
                  "geometry":{"type":"LineString","coordinates":points},
                  "properties":{"technical_code":f"SY-RD-ZA-ZAB-RD-OSM-{way_id}","osm_way_id":way_id,
                    "name_ar":tags.get("name:ar") or tags.get("name"),"name_en":tags.get("name:en"),
                    "highway":tags.get("highway"),"surface":tags.get("surface"),
                    "source":"OpenStreetMap contributors","quality_level":"D",
                    "official_status":"IMPORTED_UNVERIFIED"}})
            if "building" in tags and len(points)>=3:
                if points[0]!=points[-1]:points.append(points[0])
                handler.buildings.append({"type":"Feature","id":f"osm-building-{way_id}",
                  "geometry":{"type":"Polygon","coordinates":[points]},
                  "properties":{"technical_code":f"SY-RD-ZA-ZAB-BLD-OSM-{way_id}","osm_way_id":way_id,
                    "building_type":tags.get("building","yes"),"centroid":[lon,lat],
                    "quality_level":"D","official_status":"IMPORTED_UNVERIFIED",
                    "source":"OpenStreetMap contributors"}})
    else:
        import osmium
        class PbfExtractor(osmium.SimpleHandler,Extractor):
            def __init__(self):osmium.SimpleHandler.__init__(self);Extractor.__init__(self)
        handler=PbfExtractor();handler.apply_file(str(PBF),locations=True)
    timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    common={"license":"© OpenStreetMap contributors, ODbL 1.0",
      "source_date":timestamp,
      "notice":"Open-data working inventory. Names and geometries require municipal verification."}
    roads={"type":"FeatureCollection","name":"Al-Zabadani road working inventory",**common,
      "features":handler.roads}
    buildings={"type":"FeatureCollection","name":"Al-Zabadani building working inventory",**common,
      "features":handler.buildings}
    ROADS.write_text(json.dumps(roads,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    BUILDINGS.write_text(json.dumps(buildings,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    named=sum(bool(f["properties"].get("name_ar") or f["properties"].get("name_en")) for f in handler.roads)
    print(json.dumps({"roads":len(handler.roads),"named_roads":named,
      "buildings":len(handler.buildings),"bounds":BOUNDS}))

if __name__=="__main__":main()
