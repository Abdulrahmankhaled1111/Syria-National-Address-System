#!/usr/bin/env python3
"""Convert Maskanah building ways to traceable, unverified pilot GeoJSON."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
raw=json.loads((root/"data/import/maskanah_homs_osm_buildings.json").read_text(encoding="utf-8"))
features=[]
for item in raw.get("elements",[]):
    points=item.get("geometry") or []
    if item.get("type")!="way" or len(points)<4:
        continue
    coords=[[p["lon"],p["lat"]] for p in points]
    if coords[0]!=coords[-1]: coords.append(coords[0])
    lon=sum(p[0] for p in coords[:-1])/max(1,len(coords)-1)
    lat=sum(p[1] for p in coords[:-1])/max(1,len(coords)-1)
    features.append({"type":"Feature","id":f"osm-building-{item['id']}",
      "geometry":{"type":"Polygon","coordinates":[coords]},
      "properties":{"technical_code":f"SY-HI-HO-MAS-BLD-OSM-{item['id']}","osm_way_id":item["id"],
       "building_type":item.get("tags",{}).get("building","yes"),"centroid":[lon,lat],
       "quality_level":"D","official_status":"IMPORTED_UNVERIFIED","source":"OpenStreetMap contributors"}})
out={"type":"FeatureCollection","name":"Maskanah Homs buildings","license":"© OpenStreetMap contributors, ODbL 1.0",
     "notice":"No house numbers existed in the source export. Municipal verification required.","features":features}
(root/"data/maskanah_homs_buildings.geojson").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print(f"Wrote {len(features)} buildings")
