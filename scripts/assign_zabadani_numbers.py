"""Generate provisional odd/even house-number proposals for Al-Zabadani."""

import argparse
import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from server import SCHEMA, audit
from assign_maskanah_numbers import load_features, nearest_position


def assign(database: Path):
    roads = load_features(ROOT / "data" / "zabadani_rif_dimashq_roads.geojson")
    buildings = load_features(ROOT / "data" / "zabadani_rif_dimashq_buildings.geojson")
    grouped = {}
    for building in buildings:
        point = tuple(building["properties"]["centroid"])
        match = min(
            (
                (*nearest_position(point, road["geometry"]["coordinates"]), road)
                for road in roads
            ),
            key=lambda item: item[0],
        )
        grouped.setdefault(match[3]["id"], []).append((building, match))

    proposals = []
    for road_ref, group in grouped.items():
        counters = {"LEFT": 1, "RIGHT": 2, "UNKNOWN": 1}
        for building, match in sorted(group, key=lambda item: (item[1][1], item[0]["id"])):
            distance, progress, side, road = match
            number = counters[side]
            counters[side] += 2
            proposals.append(
                {
                    "building_ref": building["id"],
                    "road_ref": road_ref,
                    "house_number": str(number),
                    "side": side,
                    "progress": round(progress, 2),
                    "distance": round(distance, 2),
                }
            )

    stamp = datetime.now(timezone.utc).isoformat()
    batch_id = "zab-batch-" + uuid.uuid4().hex[:12]
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        connection.executescript(SCHEMA)
        existing = {
            row["building_ref"]
            for row in connection.execute(
                "SELECT building_ref FROM provisional_number_assignments"
            )
        }
        pending = [proposal for proposal in proposals if proposal["building_ref"] not in existing]
        if not pending:
            return {"created": 0, "existing": len(existing), "batch_id": None}
        connection.execute(
            "INSERT INTO numbering_batches VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (
                batch_id,
                "au-zab",
                "الزبداني",
                "Al-Zabadani",
                "NEAREST_ROAD_ODD_EVEN_V1",
                "020401",
                "MUNICIPAL_REVIEW",
                len(pending),
                len({item["road_ref"] for item in pending}),
                "usr-zab-editor",
                stamp,
            ),
        )
        for proposal in pending:
            connection.execute(
                "INSERT INTO provisional_number_assignments VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    "zab-num-" + uuid.uuid4().hex[:12],
                    batch_id,
                    proposal["building_ref"],
                    proposal["road_ref"],
                    proposal["house_number"],
                    proposal["side"],
                    proposal["progress"],
                    proposal["distance"],
                    "PROPOSED",
                    stamp,
                ),
            )
        audit(
            connection,
            "usr-zab-editor",
            "GENERATE_PROVISIONAL_NUMBERS",
            "numbering_batch",
            batch_id,
            None,
            {
                "buildings": len(pending),
                "roads_used": len({item["road_ref"] for item in pending}),
                "status": "MUNICIPAL_REVIEW",
            },
        )
    return {"created": len(pending), "existing": len(existing), "batch_id": batch_id}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(ROOT / "pilot.db"))
    args = parser.parse_args()
    print(json.dumps(assign(Path(args.db)), ensure_ascii=False, indent=2))
