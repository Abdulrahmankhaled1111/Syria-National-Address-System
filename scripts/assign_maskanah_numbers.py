"""Create provisional Maskanah house-number assignments for municipal review."""
import argparse
import json
import math
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from server import SCHEMA, audit


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def local_xy(lon, lat, latitude_origin):
    return lon * 111_320 * math.cos(math.radians(latitude_origin)), lat * 110_540


def nearest_position(point, coordinates):
    """Return distance, progress along road, and side of the nearest segment."""
    latitude_origin = point[1]
    px, py = local_xy(point[0], point[1], latitude_origin)
    best = None
    travelled = 0.0
    for start, end in zip(coordinates, coordinates[1:]):
        ax, ay = local_xy(start[0], start[1], latitude_origin)
        bx, by = local_xy(end[0], end[1], latitude_origin)
        vx, vy = bx - ax, by - ay
        length_sq = vx * vx + vy * vy
        if not length_sq:
            continue
        fraction = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / length_sq))
        qx, qy = ax + fraction * vx, ay + fraction * vy
        distance = math.hypot(px - qx, py - qy)
        segment_length = math.sqrt(length_sq)
        cross = vx * (py - qy) - vy * (px - qx)
        candidate = (distance, travelled + fraction * segment_length, "LEFT" if cross >= 0 else "RIGHT")
        if best is None or candidate[0] < best[0]:
            best = candidate
        travelled += segment_length
    return best or (float("inf"), 0.0, "UNKNOWN")


def load_features(path):
    return json.loads(path.read_text(encoding="utf-8"))["features"]


def assign(database):
    roads = load_features(ROOT / "data" / "maskanah_homs_roads.geojson")
    buildings = load_features(ROOT / "data" / "maskanah_homs_buildings.geojson")
    candidates = []
    for building in buildings:
        lon, lat = building["properties"]["centroid"]
        match = None
        for road in roads:
            distance, progress, side = nearest_position((lon, lat), road["geometry"]["coordinates"])
            if match is None or distance < match[0]:
                match = (distance, progress, side, road)
        candidates.append((building, match))

    grouped = {}
    for building, match in candidates:
        grouped.setdefault(match[3]["id"], []).append((building, match))

    assignments = []
    for road_ref, group in grouped.items():
        side_counters = {"LEFT": 1, "RIGHT": 2, "UNKNOWN": 1}
        for building, match in sorted(group, key=lambda item: (item[1][1], item[0]["id"])):
            distance, progress, side, road = match
            number = side_counters[side]
            side_counters[side] += 2
            assignments.append(
                {
                    "building_ref": building["id"],
                    "road_ref": road_ref,
                    "road": road,
                    "house_number": str(number),
                    "side": side,
                    "progress": round(progress, 2),
                    "distance": round(distance, 2),
                    "longitude": building["properties"]["centroid"][0],
                    "latitude": building["properties"]["centroid"][1],
                }
            )

    stamp = utc_now()
    batch_id = "mas-batch-" + uuid.uuid4().hex[:12]
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        connection.executescript(SCHEMA)
        existing_rows = connection.execute(
            "SELECT building_ref,road_ref,side,house_number FROM provisional_number_assignments"
        ).fetchall()
        existing_refs = {row["building_ref"] for row in existing_rows}
        used = {}
        for row in existing_rows:
            used.setdefault((row["road_ref"], row["side"]), set()).add(int(row["house_number"]))
        pending = [item for item in assignments if item["building_ref"] not in existing_refs]
        if not pending:
            return {"created": 0, "existing": len(existing_rows), "batch_id": None, "roads_used": 0}
        for item in pending:
            key = (item["road_ref"], item["side"])
            occupied = used.setdefault(key, set())
            number = int(item["house_number"])
            while number in occupied:
                number += 2
            item["house_number"] = str(number)
            occupied.add(number)
        pending_roads = {item["road_ref"] for item in pending}
        connection.execute(
            "INSERT INTO numbering_batches VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (
                batch_id,
                "au-mas",
                "مسكنة",
                "Maskanah",
                "NEAREST_ROAD_ODD_EVEN_V1",
                "010101",
                "MUNICIPAL_REVIEW",
                len(pending),
                len(pending_roads),
                "usr-mas-editor",
                stamp,
            ),
        )
        for assignment in pending:
            road_properties = assignment["road"]["properties"]
            road_code = road_properties["technical_code"]
            street_ar = road_properties.get("name_ar") or f"طريق غير مسمى {road_code}"
            street_en = road_properties.get("name_en") or f"Unnamed road {road_code}"
            assignment_id = "mas-num-" + uuid.uuid4().hex[:12]
            case_id = "mas-case-" + uuid.uuid4().hex[:12]
            connection.execute(
                "INSERT INTO provisional_number_assignments VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    assignment_id,
                    batch_id,
                    assignment["building_ref"],
                    assignment["road_ref"],
                    assignment["house_number"],
                    assignment["side"],
                    assignment["progress"],
                    assignment["distance"],
                    "SUBMITTED",
                    stamp,
                ),
            )
            connection.execute(
                "INSERT INTO house_number_cases VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    case_id,
                    assignment["building_ref"],
                    "مسكنة",
                    "Maskanah",
                    street_ar,
                    street_en,
                    assignment["house_number"],
                    "010101",
                    assignment["longitude"],
                    assignment["latitude"],
                    "SUBMITTED",
                    "usr-mas-editor",
                    None,
                    None,
                    stamp,
                    stamp,
                ),
            )
        audit(
            connection,
            "usr-mas-editor",
            "GENERATE_PROVISIONAL_NUMBERS",
            "numbering_batch",
            batch_id,
            None,
            {"buildings": len(pending), "roads_used": len(pending_roads)},
        )
    return {"created": len(pending), "existing": len(existing_rows), "batch_id": batch_id, "roads_used": len(pending_roads)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(ROOT / "pilot.db"))
    args = parser.parse_args()
    print(json.dumps(assign(Path(args.db)), ensure_ascii=False, indent=2))
