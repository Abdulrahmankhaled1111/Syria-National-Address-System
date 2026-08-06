#!/usr/bin/env python3
"""Convert the bounded Overpass export to pilot GeoJSON."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
raw=json.loads((root/"data/import/maskanah_homs_osm_roads.json").read_text(encoding="utf-8"))
features=[]
for item in raw.get("elements",[]):
    geometry=item.get("geometry") or []
    if item.get("type")!="way" or len(geometry)<2:
        continue
    tags=item.get("tags",{})
    features.append({"type":"Feature","id":f"osm-way-{item['id']}",
      "geometry":{"type":"LineString","coordinates":[[p["lon"],p["lat"]] for p in geometry]},
      "properties":{"technical_code":f"SY-HI-HO-MAS-OSM-{item['id']}","osm_way_id":item["id"],
        "name_ar":tags.get("name:ar") or tags.get("name"),"name_en":tags.get("name:en"),
        "highway":tags.get("highway"),"surface":tags.get("surface"),
        "source":"OpenStreetMap contributors","source_date":raw.get("osm3s",{}).get("timestamp_osm_base"),
        "quality_level":"D","official_status":"IMPORTED_UNVERIFIED"}})
collection={"type":"FeatureCollection","name":"Maskanah Homs road pilot",
 "license":"© OpenStreetMap contributors, ODbL 1.0",
 "notice":"Not official. Municipal field verification and naming decision required.","features":features}
(root/"data/maskanah_homs_roads.geojson").write_text(json.dumps(collection,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print(f"Wrote {len(features)} road segments")
