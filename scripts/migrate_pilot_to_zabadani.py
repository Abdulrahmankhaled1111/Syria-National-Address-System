#!/usr/bin/env python3
"""Replace the former Maskanah pilot inventory with the Al-Zabadani pilot."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "pilot.db"
ROADS = ROOT / "data" / "zabadani_rif_dimashq_roads.geojson"
BUILDINGS = ROOT / "data" / "zabadani_rif_dimashq_buildings.geojson"


def stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def password_hash(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"sna-pilot", 120_000).hex()


def audit(conn: sqlite3.Connection, action: str, after: dict) -> None:
    previous = conn.execute(
        "SELECT chain_hash FROM audit_log ORDER BY id DESC LIMIT 1"
    ).fetchone()
    event_time = stamp()
    material = "|".join(
        [
            previous[0] if previous else "GENESIS",
            event_time,
            "usr-admin",
            action,
            "PILOT_AREA",
            "au-zab",
            json.dumps(None, sort_keys=True),
            json.dumps(after, sort_keys=True),
        ]
    )
    chain_hash = hashlib.sha256(material.encode()).hexdigest()
    conn.execute(
        """INSERT INTO audit_log
           (event_time,actor_id,action,object_type,object_id,before_json,after_json,chain_hash)
           VALUES(?,?,?,?,?,?,?,?)""",
        (
            event_time,
            "usr-admin",
            action,
            "PILOT_AREA",
            "au-zab",
            json.dumps(None),
            json.dumps(after),
            chain_hash,
        ),
    )


def main() -> None:
    roads = json.loads(ROADS.read_text(encoding="utf-8"))["features"]
    buildings = json.loads(BUILDINGS.read_text(encoding="utf-8"))["features"]
    created = stamp()
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        with conn:
            # Remove the former local pilot data and accounts in dependency order.
            mask_users = [
                row[0]
                for row in conn.execute(
                    "SELECT id FROM users WHERE username LIKE 'maskanah.%'"
                )
            ]
            if mask_users:
                marks = ",".join("?" for _ in mask_users)
                conn.execute(
                    f"DELETE FROM staff_admin_scopes WHERE user_id IN ({marks})",
                    mask_users,
                )
                conn.execute(
                    f"DELETE FROM staff_profiles WHERE user_id IN ({marks})", mask_users
                )
                conn.execute(f"DELETE FROM users WHERE id IN ({marks})", mask_users)
            conn.execute("DELETE FROM object_dossiers WHERE admin_unit_id='au-mas'")
            conn.execute("DELETE FROM road_catalog")
            conn.execute("DELETE FROM building_catalog")
            conn.execute("DELETE FROM postal_areas WHERE admin_unit_id='au-mas'")
            conn.execute("DELETE FROM admin_units WHERE id='au-mas'")
            conn.execute(
                "DELETE FROM system_settings WHERE setting_key='maskanah_roads_enabled'"
            )

            units = [
                ("au-rd", "SY-RD", "GOVERNORATE", None, "ريف دمشق", "Rif Dimashq"),
                ("au-za", "SY-RD-ZA", "DISTRICT", "au-rd", "منطقة الزبداني", "Al-Zabadani District"),
                ("au-zab", "SY-RD-ZA-ZAB", "MUNICIPALITY", "au-za", "مدينة الزبداني", "Al-Zabadani Municipality"),
            ]
            for unit in units:
                conn.execute(
                    """INSERT INTO admin_units(id,code,level,parent_id,name_ar,name_en,status)
                       VALUES(?,?,?,?,?,?,'ACTIVE')
                       ON CONFLICT(id) DO UPDATE SET code=excluded.code,level=excluded.level,
                       parent_id=excluded.parent_id,name_ar=excluded.name_ar,
                       name_en=excluded.name_en,status='ACTIVE'""",
                    unit,
                )

            # These are project draft codes pending legal adoption by the competent authority.
            conn.execute(
                """INSERT INTO postal_areas
                   (postal_code,admin_unit_id,locality_ar,locality_en,locality_de,status,valid_from)
                   VALUES('010101','au-md','دمشق','Damascus','Damaskus','DRAFT',?)
                   ON CONFLICT(postal_code) DO UPDATE SET admin_unit_id='au-md',
                   locality_ar='دمشق',locality_en='Damascus',locality_de='Damaskus',
                   status='DRAFT'""",
                (created,),
            )
            conn.execute(
                """INSERT INTO postal_areas
                   (postal_code,admin_unit_id,locality_ar,locality_en,locality_de,status,valid_from)
                   VALUES('020401','au-zab','الزبداني','Al-Zabadani','Al-Zabadani','DRAFT',?)
                   ON CONFLICT(postal_code) DO UPDATE SET admin_unit_id='au-zab',
                   locality_ar='الزبداني',locality_en='Al-Zabadani',
                   locality_de='Al-Zabadani',status='DRAFT'""",
                (created,),
            )

            accounts = [
                ("usr-zab-editor", "zabadani.editor", "Rathaus Al-Zabadani", "EDITOR", "Zabadani123!", "MUNICIPAL_EDITOR"),
                ("usr-zab-surveyor", "zabadani.surveyor", "Vermessung Al-Zabadani", "EDITOR", "ZabSurvey123!", "SURVEYOR"),
                ("usr-zab-reviewer", "zabadani.reviewer", "Prüfung Al-Zabadani", "REVIEWER", "ZabReview123!", "REVIEWER"),
                ("usr-zab-approver", "zabadani.approver", "Genehmigung Al-Zabadani", "APPROVER", "ZabApprove123!", "APPROVER"),
                ("usr-zab-installer", "zabadani.installer", "Außendienst Al-Zabadani", "EDITOR", "ZabInstall123!", "INSTALLER"),
            ]
            for user_id, username, display, role, password, operational_role in accounts:
                conn.execute(
                    """INSERT INTO users(id,username,display_name,role,password_hash,active)
                       VALUES(?,?,?,?,?,1)
                       ON CONFLICT(id) DO UPDATE SET username=excluded.username,
                       display_name=excluded.display_name,role=excluded.role,
                       password_hash=excluded.password_hash,active=1""",
                    (user_id, username, display, role, password_hash(password)),
                )
                conn.execute(
                    """INSERT INTO staff_profiles
                       (user_id,operational_role,organisation,admin_unit_id,active)
                       VALUES(?,?,'Municipality of Al-Zabadani','au-zab',1)
                       ON CONFLICT(user_id) DO UPDATE SET
                       operational_role=excluded.operational_role,
                       organisation=excluded.organisation,admin_unit_id='au-zab',active=1""",
                    (user_id, operational_role),
                )
                conn.execute(
                    """INSERT OR REPLACE INTO staff_admin_scopes
                       (user_id,admin_unit_id,can_edit,assigned_at)
                       VALUES(?,'au-zab',1,?)""",
                    (user_id, created),
                )

            for feature in roads:
                props = feature["properties"]
                ref = feature["id"]
                code = props["technical_code"]
                conn.execute(
                    """INSERT INTO road_catalog
                       (id,technical_code,name_ar,name_en,aliases,highway,geometry_geojson,
                        source,quality_level,official_status)
                       VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (
                        ref,
                        code,
                        props.get("name_ar"),
                        props.get("name_en"),
                        "[]",
                        props.get("highway"),
                        json.dumps(feature["geometry"]),
                        props["source"],
                        props["quality_level"],
                        props["official_status"],
                    ),
                )
                conn.execute(
                    """INSERT INTO object_dossiers
                       (dossier_number,object_type,object_ref,admin_unit_id,status,metadata,created_at,updated_at)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (
                        code.replace("-OSM-", "-"),
                        "ROAD",
                        ref,
                        "au-zab",
                        "OPEN",
                        json.dumps({"verification": "MUNICIPAL_REVIEW_REQUIRED"}),
                        created,
                        created,
                    ),
                )

            for feature in buildings:
                props = feature["properties"]
                ref = feature["id"]
                code = props["technical_code"]
                lon, lat = props["centroid"]
                conn.execute(
                    """INSERT INTO building_catalog
                       (id,technical_code,geometry_geojson,longitude,latitude,source,
                        quality_level,official_status)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (
                        ref,
                        code,
                        json.dumps(feature["geometry"]),
                        lon,
                        lat,
                        props["source"],
                        props["quality_level"],
                        props["official_status"],
                    ),
                )
                conn.execute(
                    """INSERT INTO object_dossiers
                       (dossier_number,object_type,object_ref,admin_unit_id,status,metadata,created_at,updated_at)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (
                        code.replace("-OSM-", "-"),
                        "BUILDING",
                        ref,
                        "au-zab",
                        "OPEN",
                        json.dumps({"verification": "FIELD_CHECK_REQUIRED"}),
                        created,
                        created,
                    ),
                )

            conn.execute(
                """INSERT INTO system_settings(setting_key,setting_value,updated_by,updated_at)
                   VALUES('zabadani_roads_enabled','true','usr-admin',?)
                   ON CONFLICT(setting_key) DO UPDATE SET setting_value='true',
                   updated_by='usr-admin',updated_at=excluded.updated_at""",
                (created,),
            )
            audit(
                conn,
                "REPLACE_PILOT_AREA",
                {
                    "removed": "Maskanah",
                    "active": "Al-Zabadani",
                    "roads": len(roads),
                    "named_road_segments": sum(
                        1
                        for feature in roads
                        if feature["properties"].get("name_ar")
                        or feature["properties"].get("name_en")
                    ),
                    "buildings": len(buildings),
                    "postal_code": "020401",
                    "postal_status": "DRAFT",
                    "house_numbers_assigned": 0,
                },
            )
    finally:
        conn.close()
    print(
        json.dumps(
            {
                "removed": "Maskanah",
                "active": "Al-Zabadani",
                "roads": len(roads),
                "buildings": len(buildings),
                "postal_code": "020401",
                "house_numbers_assigned": 0,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
