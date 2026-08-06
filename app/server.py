#!/usr/bin/env python3
"""Syrian National Address Pilot - dependency-free reference API.

The local demo uses SQLite so it can be evaluated without infrastructure.
Production deployment uses the PostgreSQL/PostGIS schema in db/migrations.
"""
from __future__ import annotations

import argparse
import csv
import io
import math
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from xml.sax.saxutils import escape as xml_escape
from pdf_dossier import build_pdf, build_cadastral_map_pdf

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
DATA = ROOT / "data"
NATIONAL_DB = DATA / "national" / "syria_catalog.sqlite"
PILOT_UNIT_ID="au-zab"
SYRIA_GOVERNORATES=[
    ("au-di","SY-01-DI","دمشق","Damascus",36.291,33.513,10.0),
    ("au-rd","SY-02-RD","ريف دمشق","Rif Dimashq",36.30,33.55,8.2),
    ("au-al","SY-03-AL","حلب","Aleppo",37.16,36.20,8.0),
    ("au-hi","SY-04-HI","حمص","Homs",36.72,34.73,8.0),
    ("au-hm","SY-05-HM","حماة","Hama",36.75,35.13,8.2),
    ("au-la","SY-06-LA","اللاذقية","Latakia",35.78,35.52,8.5),
    ("au-ta","SY-07-TA","طرطوس","Tartus",35.89,34.89,8.7),
    ("au-id","SY-08-ID","إدلب","Idlib",36.63,35.93,8.3),
    ("au-ra","SY-09-RA","الرقة","Raqqa",39.01,35.95,8.0),
    ("au-dz","SY-10-DZ","دير الزور","Deir ez-Zor",40.14,35.34,7.8),
    ("au-ha","SY-11-HA","الحسكة","Al-Hasakah",40.75,36.50,7.6),
    ("au-dr","SY-12-DR","درعا","Daraa",36.10,32.62,8.5),
    ("au-su","SY-13-SU","السويداء","As-Suwayda",36.57,32.71,8.5),
    ("au-qu","SY-14-QU","القنيطرة","Quneitra",35.82,33.12,8.8),
]
PILOT_LOCALITY_AR="الزبداني"
PILOT_LOCALITY_EN="Al-Zabadani"
PILOT_POSTAL_CODE="020401"
PILOT_ROADS=DATA/"zabadani_rif_dimashq_roads.geojson"
PILOT_BUILDINGS=DATA/"zabadani_rif_dimashq_buildings.geojson"
GOVERNORATE_BOUNDARIES=DATA/"syria_governorates.geojson"
GOVERNORATE_SOURCE_ISO={
    "au-di":"SY-DI","au-rd":"SY-RD","au-al":"SY-HL","au-hi":"SY-HI",
    "au-hm":"SY-HM","au-la":"SY-LA","au-ta":"SY-TA","au-id":"SY-ID",
    "au-ra":"SY-RA","au-dz":"SY-DY","au-ha":"SY-HA","au-dr":"SY-DR",
    "au-su":"SY-SU","au-qu":"SY-QU",
}
DB_PATH = Path(os.getenv("SNA_DB_PATH", ROOT / "pilot.db"))
TOKEN_SECRET = os.getenv("SNA_TOKEN_SECRET", "pilot-only-change-me").encode()
APP_ENV = os.getenv("SNA_ENV", "development").lower()
TOKEN_TTL_SECONDS = int(os.getenv("SNA_TOKEN_TTL_SECONDS", "28800"))
ALLOWED_HOSTS = {value.strip() for value in os.getenv("SNA_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if value.strip()}
JSON_HEADERS = {"Content-Type": "application/json; charset=utf-8"}
LOGIN_FAILURES = {}
LOGIN_LOCK = threading.Lock()
REQUEST_CONTEXT = threading.local()
LOGIN_WINDOW_SECONDS = 900
LOGIN_MAX_FAILURES = 5

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS users (
 id TEXT PRIMARY KEY, username TEXT UNIQUE NOT NULL, display_name TEXT NOT NULL,
 role TEXT NOT NULL CHECK(role IN ('PUBLIC','EDITOR','REVIEWER','APPROVER','AUDITOR','ADMIN')),
 password_hash TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS staff_profiles (
 user_id TEXT PRIMARY KEY REFERENCES users(id), operational_role TEXT NOT NULL,
 organisation TEXT NOT NULL, admin_unit_id TEXT, active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS staff_admin_scopes (
 user_id TEXT NOT NULL REFERENCES users(id), admin_unit_id TEXT NOT NULL REFERENCES admin_units(id),
 can_edit INTEGER NOT NULL DEFAULT 1, assigned_at TEXT NOT NULL,
 PRIMARY KEY(user_id,admin_unit_id)
);
CREATE TABLE IF NOT EXISTS admin_units (
 id TEXT PRIMARY KEY, code TEXT UNIQUE NOT NULL, level TEXT NOT NULL,
 parent_id TEXT REFERENCES admin_units(id), name_ar TEXT NOT NULL, name_en TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'ACTIVE'
);
CREATE TABLE IF NOT EXISTS streets (
 id TEXT PRIMARY KEY, official_code TEXT UNIQUE NOT NULL, admin_unit_id TEXT NOT NULL REFERENCES admin_units(id),
 name_ar TEXT NOT NULL, name_en TEXT, former_names TEXT NOT NULL DEFAULT '[]',
 status TEXT NOT NULL DEFAULT 'ACTIVE'
);
CREATE TABLE IF NOT EXISTS buildings (
 id TEXT PRIMARY KEY, official_code TEXT UNIQUE NOT NULL, admin_unit_id TEXT NOT NULL REFERENCES admin_units(id),
 geometry_geojson TEXT NOT NULL, function_code TEXT NOT NULL, lifecycle_status TEXT NOT NULL,
 floors INTEGER, dwelling_units INTEGER, quality_level TEXT NOT NULL, source_type TEXT NOT NULL,
 valid_from TEXT NOT NULL, valid_to TEXT, version INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS addresses (
 id TEXT PRIMARY KEY, official_code TEXT UNIQUE NOT NULL, street_id TEXT REFERENCES streets(id),
 building_id TEXT REFERENCES buildings(id), house_number TEXT, postal_code TEXT,
 entrance_label TEXT, name_ar TEXT NOT NULL, name_en TEXT,
 longitude REAL NOT NULL, latitude REAL NOT NULL,
 quality_level TEXT NOT NULL, official_status TEXT NOT NULL DEFAULT 'OFFICIAL',
 valid_from TEXT NOT NULL, valid_to TEXT, version INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS change_requests (
 id TEXT PRIMARY KEY, object_type TEXT NOT NULL, object_id TEXT, operation TEXT NOT NULL,
 payload TEXT NOT NULL, reason TEXT NOT NULL, status TEXT NOT NULL,
 requested_by TEXT NOT NULL REFERENCES users(id), reviewed_by TEXT REFERENCES users(id),
 approved_by TEXT REFERENCES users(id), created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_log (
 id INTEGER PRIMARY KEY AUTOINCREMENT, event_time TEXT NOT NULL, actor_id TEXT,
 action TEXT NOT NULL, object_type TEXT NOT NULL, object_id TEXT,
 before_json TEXT, after_json TEXT, chain_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS field_jobs (
 id TEXT PRIMARY KEY, address_id TEXT NOT NULL REFERENCES addresses(id),
 job_type TEXT NOT NULL CHECK(job_type IN ('PLAN_EXPORT','NOTICE_LETTER','PLAQUE_PRODUCTION','PLAQUE_INSTALLATION')),
 status TEXT NOT NULL CHECK(status IN ('CREATED','ASSIGNED','PRINTED','IN_PRODUCTION','READY','INSTALLED','VERIFIED','CANCELLED')),
 assigned_to TEXT REFERENCES users(id), created_by TEXT NOT NULL REFERENCES users(id),
 payload TEXT NOT NULL DEFAULT '{}', evidence TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS postal_areas (
 postal_code TEXT PRIMARY KEY, admin_unit_id TEXT NOT NULL REFERENCES admin_units(id),
 locality_ar TEXT NOT NULL, locality_en TEXT NOT NULL, locality_de TEXT,
 status TEXT NOT NULL DEFAULT 'DRAFT', valid_from TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS house_number_cases (
 id TEXT PRIMARY KEY, building_ref TEXT NOT NULL, locality_ar TEXT NOT NULL, locality_en TEXT NOT NULL,
 street_name_ar TEXT NOT NULL, street_name_en TEXT, house_number TEXT NOT NULL, postal_code TEXT NOT NULL,
 longitude REAL NOT NULL, latitude REAL NOT NULL, status TEXT NOT NULL,
 requested_by TEXT NOT NULL REFERENCES users(id), reviewed_by TEXT REFERENCES users(id),
 approved_by TEXT REFERENCES users(id), created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 floors INTEGER, dwelling_units INTEGER, street_side TEXT NOT NULL DEFAULT 'UNDETERMINED',
  UNIQUE(building_ref,status)
);
CREATE TABLE IF NOT EXISTS system_settings (
 setting_key TEXT PRIMARY KEY, setting_value TEXT NOT NULL, updated_by TEXT,
 updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS support_tickets (
 id TEXT PRIMARY KEY, category TEXT NOT NULL, subject TEXT NOT NULL, message TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'OPEN', created_by TEXT NOT NULL REFERENCES users(id),
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS numbering_batches (
 id TEXT PRIMARY KEY, admin_unit_id TEXT NOT NULL, locality_ar TEXT NOT NULL,
 locality_en TEXT NOT NULL, method TEXT NOT NULL, postal_code TEXT NOT NULL,
 status TEXT NOT NULL, building_count INTEGER NOT NULL, road_count INTEGER NOT NULL,
 created_by TEXT NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS provisional_number_assignments (
 id TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES numbering_batches(id),
 building_ref TEXT NOT NULL UNIQUE, road_ref TEXT NOT NULL,
 house_number TEXT NOT NULL, side TEXT NOT NULL, sequence_m REAL NOT NULL,
 distance_to_road_m REAL NOT NULL, status TEXT NOT NULL,
 created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS installation_evidence (
 id TEXT PRIMARY KEY, house_number_case_id TEXT NOT NULL UNIQUE REFERENCES house_number_cases(id),
 installed_by TEXT NOT NULL REFERENCES users(id), plaque_installed INTEGER NOT NULL,
 mailbox_installed INTEGER NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL,
 photo_data TEXT, device_time TEXT NOT NULL, server_time TEXT NOT NULL,
 verification_status TEXT NOT NULL DEFAULT 'PENDING',
 gps_accuracy_m REAL, entrance_latitude REAL, entrance_longitude REAL,
 entrance_adjusted INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS road_catalog (
 id TEXT PRIMARY KEY, technical_code TEXT UNIQUE NOT NULL, name_ar TEXT, name_en TEXT,
 aliases TEXT NOT NULL DEFAULT '[]', highway TEXT, geometry_geojson TEXT NOT NULL,
 source TEXT NOT NULL, quality_level TEXT NOT NULL, official_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS building_catalog (
 id TEXT PRIMARY KEY, technical_code TEXT UNIQUE NOT NULL, geometry_geojson TEXT NOT NULL,
 longitude REAL NOT NULL, latitude REAL NOT NULL, source TEXT NOT NULL,
 quality_level TEXT NOT NULL, official_status TEXT NOT NULL,
 admin_unit_id TEXT REFERENCES admin_units(id), parcel_id TEXT REFERENCES parcels(id),
 object_number TEXT, created_by TEXT REFERENCES users(id), created_at TEXT
);
CREATE TABLE IF NOT EXISTS object_dossiers (
 dossier_number TEXT PRIMARY KEY, object_type TEXT NOT NULL, object_ref TEXT NOT NULL,
 admin_unit_id TEXT NOT NULL, status TEXT NOT NULL, metadata TEXT NOT NULL DEFAULT '{}',
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL, UNIQUE(object_type,object_ref)
);
CREATE TABLE IF NOT EXISTS building_entrances (
 id TEXT PRIMARY KEY, building_ref TEXT NOT NULL, entrance_label TEXT NOT NULL,
 longitude REAL, latitude REAL, status TEXT NOT NULL DEFAULT 'DRAFT',
 created_at TEXT NOT NULL, UNIQUE(building_ref,entrance_label)
);
CREATE TABLE IF NOT EXISTS residential_units (
 id TEXT PRIMARY KEY, building_ref TEXT NOT NULL, entrance_id TEXT REFERENCES building_entrances(id),
 unit_number TEXT NOT NULL, floor_label TEXT, usage_type TEXT NOT NULL DEFAULT 'RESIDENTIAL',
 status TEXT NOT NULL DEFAULT 'DRAFT', created_at TEXT NOT NULL,
 UNIQUE(building_ref,entrance_id,unit_number)
);
CREATE TABLE IF NOT EXISTS population_persons (
 id TEXT PRIMARY KEY, register_number TEXT UNIQUE NOT NULL, given_names TEXT NOT NULL,
 family_name TEXT NOT NULL, birth_date TEXT, protection_flag INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resident_registrations (
 id TEXT PRIMARY KEY, person_id TEXT NOT NULL REFERENCES population_persons(id),
 unit_id TEXT NOT NULL REFERENCES residential_units(id), residence_type TEXT NOT NULL,
 move_in_date TEXT NOT NULL, move_out_date TEXT, status TEXT NOT NULL DEFAULT 'ACTIVE',
 registered_by TEXT NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cadastral_districts (
 id TEXT PRIMARY KEY, admin_unit_id TEXT NOT NULL REFERENCES admin_units(id),
 district_code TEXT UNIQUE NOT NULL, name_ar TEXT NOT NULL, name_en TEXT,
 official_status TEXT NOT NULL DEFAULT 'DRAFT'
);
CREATE TABLE IF NOT EXISTS cadastral_sections (
 id TEXT PRIMARY KEY, cadastral_district_id TEXT NOT NULL REFERENCES cadastral_districts(id),
 section_number TEXT NOT NULL, name_ar TEXT, geometry_geojson TEXT,
 official_status TEXT NOT NULL DEFAULT 'DRAFT',
 UNIQUE(cadastral_district_id,section_number)
);
CREATE TABLE IF NOT EXISTS parcels (
 id TEXT PRIMARY KEY, cadastral_section_id TEXT NOT NULL REFERENCES cadastral_sections(id),
 parcel_number TEXT NOT NULL, geometry_geojson TEXT NOT NULL,
 quality_level TEXT NOT NULL, official_status TEXT NOT NULL DEFAULT 'DRAFT',
 UNIQUE(cadastral_section_id,parcel_number)
);
CREATE TABLE IF NOT EXISTS parcel_building_links (
 parcel_id TEXT NOT NULL REFERENCES parcels(id), building_ref TEXT NOT NULL,
 relation_type TEXT NOT NULL DEFAULT 'CONTAINS', valid_from TEXT NOT NULL,
 valid_to TEXT, created_by TEXT NOT NULL REFERENCES users(id),
 PRIMARY KEY(parcel_id,building_ref,valid_from)
);
"""

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def seed_governorates(conn):
    conn.executemany("""INSERT OR IGNORE INTO admin_units
        (id,code,level,parent_id,name_ar,name_en,status)
        VALUES(?,?,'GOVERNORATE','au-sy',?,?, 'ACTIVE')""",
        [(unit_id,code,name_ar,name_en) for unit_id,code,name_ar,name_en,_,_,_ in SYRIA_GOVERNORATES])
    conn.executemany("""UPDATE admin_units SET code=?,level='GOVERNORATE',
        parent_id='au-sy',name_ar=?,name_en=?,status='ACTIVE' WHERE id=?""",
        [(code,name_ar,name_en,unit_id) for unit_id,code,name_ar,name_en,_,_,_ in SYRIA_GOVERNORATES])

def governorate_features():
    if not GOVERNORATE_BOUNDARIES.exists():return []
    features=json.loads(GOVERNORATE_BOUNDARIES.read_text(encoding="utf-8")).get("features",[])
    by_iso={value:key for key,value in GOVERNORATE_SOURCE_ISO.items()}
    result=[]
    for feature in features:
        unit_id=by_iso.get(feature.get("properties",{}).get("shapeISO"))
        if not unit_id:continue
        copy=json.loads(json.dumps(feature))
        copy["id"]=unit_id
        copy["properties"]["admin_unit_id"]=unit_id
        result.append(copy)
    return result

def point_in_ring(longitude,latitude,ring):
    inside=False
    j=len(ring)-1
    for i,(x,y,*_) in enumerate(ring):
        xj,yj=ring[j][0],ring[j][1]
        if ((y>latitude)!=(yj>latitude)) and longitude < (xj-x)*(latitude-y)/(yj-y or 1e-15)+x:
            inside=not inside
        j=i
    return inside

def point_in_geometry(longitude,latitude,geometry):
    polygons=geometry.get("coordinates",[])
    if geometry.get("type")=="Polygon":polygons=[polygons]
    if geometry.get("type") not in {"Polygon","MultiPolygon"}:return False
    for polygon in polygons:
        if polygon and point_in_ring(longitude,latitude,polygon[0]) and not any(
            point_in_ring(longitude,latitude,hole) for hole in polygon[1:]):
            return True
    return False

def assigned_governorate(conn,user_id):
    row=conn.execute("""WITH RECURSIVE ancestors(id,parent_id,level) AS (
        SELECT a.id,a.parent_id,a.level FROM admin_units a
        JOIN staff_profiles p ON p.admin_unit_id=a.id WHERE p.user_id=?
        UNION ALL
        SELECT parent.id,parent.parent_id,parent.level FROM admin_units parent
        JOIN ancestors child ON child.parent_id=parent.id)
        SELECT id FROM ancestors WHERE level='GOVERNORATE' LIMIT 1""",(user_id,)).fetchone()
    return row["id"] if row else None

def scoped_admin_unit_ids(conn,admin_unit_id):
    """Return an administrative unit and all of its descendants."""
    return [row["id"] for row in conn.execute("""WITH RECURSIVE units(id) AS (
        SELECT id FROM admin_units WHERE id=?
        UNION ALL
        SELECT child.id FROM admin_units child JOIN units parent ON child.parent_id=parent.id)
        SELECT id FROM units""",(admin_unit_id,)).fetchall()]

def validate_production_config():
    problems=[]
    if APP_ENV!="production":return problems
    if len(TOKEN_SECRET)<32 or TOKEN_SECRET in (b"pilot-only-change-me",b"development-change-this-secret"):
        problems.append("SNA_TOKEN_SECRET must contain at least 32 random characters")
    if not ALLOWED_HOSTS:problems.append("SNA_ALLOWED_HOSTS must not be empty")
    if TOKEN_TTL_SECONDS<300 or TOKEN_TTL_SECONDS>43200:
        problems.append("SNA_TOKEN_TTL_SECONDS must be between 300 and 43200")
    bootstrap=os.getenv("SNA_BOOTSTRAP_ADMIN_PASSWORD","")
    if len(bootstrap)<14:
        problems.append("SNA_BOOTSTRAP_ADMIN_PASSWORD must contain at least 14 characters")
    return problems

def login_allowed(key):
    cutoff=time.time()-LOGIN_WINDOW_SECONDS
    with LOGIN_LOCK:
        recent=[stamp for stamp in LOGIN_FAILURES.get(key,[]) if stamp>=cutoff]
        LOGIN_FAILURES[key]=recent
        return len(recent)<LOGIN_MAX_FAILURES

def login_failed(key):
    with LOGIN_LOCK:LOGIN_FAILURES.setdefault(key,[]).append(time.time())

def login_succeeded(key):
    with LOGIN_LOCK:LOGIN_FAILURES.pop(key,None)

def password_hash(password: str, salt: str = "sna-pilot") -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000).hex()

def secure_password_hash(password):
    salt=secrets.token_bytes(16)
    digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1,dklen=32)
    return f"scrypt$16384$8$1${salt.hex()}${digest.hex()}"

def verify_password(stored,password):
    if stored.startswith("scrypt$"):
        try:
            _,n,r,p,salt,digest=stored.split("$")
            actual=hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt),n=int(n),r=int(r),p=int(p),dklen=32)
            return hmac.compare_digest(actual.hex(),digest)
        except (ValueError,TypeError):
            return False
    return hmac.compare_digest(stored,password_hash(password))

def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def national_db() -> sqlite3.Connection:
    conn=sqlite3.connect(f"file:{NATIONAL_DB}?mode=ro",uri=True)
    conn.row_factory=sqlite3.Row
    return conn

def audit(conn, actor, action, obj_type, obj_id, before=None, after=None):
    previous = conn.execute("SELECT chain_hash FROM audit_log ORDER BY id DESC LIMIT 1").fetchone()
    stamp=now()
    capture=getattr(REQUEST_CONTEXT,"value",None)
    stored_after={"data":after,"capture":capture} if capture else after
    material = "|".join([previous["chain_hash"] if previous else "GENESIS", stamp, actor or "",
                         action, obj_type, obj_id or "", json.dumps(before, sort_keys=True),
                         json.dumps(stored_after, sort_keys=True)])
    chain = hashlib.sha256(material.encode()).hexdigest()
    conn.execute("""INSERT INTO audit_log(event_time,actor_id,action,object_type,object_id,before_json,after_json,chain_hash)
                    VALUES(?,?,?,?,?,?,?,?)""",
                 (stamp, actor, action, obj_type, obj_id, json.dumps(before), json.dumps(stored_after), chain))

def audit_chain_status(conn):
    previous="GENESIS"
    checked=0
    for row in conn.execute("SELECT * FROM audit_log ORDER BY id"):
        before=json.loads(row["before_json"]) if row["before_json"] else None
        after=json.loads(row["after_json"]) if row["after_json"] else None
        material="|".join([previous,row["event_time"],row["actor_id"] or "",row["action"],
            row["object_type"],row["object_id"] or "",json.dumps(before,sort_keys=True),
            json.dumps(after,sort_keys=True)])
        expected=hashlib.sha256(material.encode()).hexdigest()
        if not hmac.compare_digest(expected,row["chain_hash"]):
            return {"valid":False,"checked":checked,"failed_id":row["id"]}
        previous=row["chain_hash"]
        checked+=1
    return {"valid":True,"checked":checked,"head":previous}

def sync_catalog(conn):
    enabled=conn.execute("""SELECT setting_value FROM system_settings
        WHERE setting_key='zabadani_roads_enabled'""").fetchone()
    roads_enabled=not enabled or enabled["setting_value"].lower()=="true"
    roads_file=PILOT_ROADS
    if roads_enabled and roads_file.exists():
        for f in json.loads(roads_file.read_text(encoding="utf-8"))["features"]:
            p=f["properties"]
            conn.execute("INSERT OR IGNORE INTO road_catalog VALUES(?,?,?,?,?,?,?,?,?,?)",
              (f["id"],p["technical_code"],p.get("name_ar"),p.get("name_en"),"[]",p.get("highway"),
               json.dumps(f["geometry"]),p["source"],p["quality_level"],p["official_status"]))
            conn.execute("INSERT OR IGNORE INTO object_dossiers VALUES(?,?,?,?,?,?,?,?)",
              (f"SY-RD-ZA-ZAB-RD-{p['osm_way_id']}", "ROAD",f["id"],PILOT_UNIT_ID,"OPEN",
               json.dumps({"source":p["source"],"quality":p["quality_level"]}),now(),now()))
    buildings_file=PILOT_BUILDINGS
    if buildings_file.exists():
        for f in json.loads(buildings_file.read_text(encoding="utf-8"))["features"]:
            p=f["properties"]; lon,lat=p["centroid"]
            conn.execute("""INSERT OR IGNORE INTO building_catalog
              (id,technical_code,geometry_geojson,longitude,latitude,source,quality_level,official_status)
              VALUES(?,?,?,?,?,?,?,?)""",
              (f["id"],p["technical_code"],json.dumps(f["geometry"]),lon,lat,p["source"],
               p["quality_level"],p["official_status"]))
            conn.execute("INSERT OR IGNORE INTO object_dossiers VALUES(?,?,?,?,?,?,?,?)",
              (f"SY-RD-ZA-ZAB-BLD-{p['osm_way_id']}","BUILDING",f["id"],PILOT_UNIT_ID,"OPEN",
               json.dumps({"source":p["source"],"quality":p["quality_level"]}),now(),now()))

def init_db(reset=False):
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    with db() as conn:
        conn.executescript(SCHEMA)
        evidence_columns={row["name"] for row in conn.execute("PRAGMA table_info(installation_evidence)")}
        for column,definition in (
            ("gps_accuracy_m","REAL"),
            ("entrance_latitude","REAL"),
            ("entrance_longitude","REAL"),
            ("entrance_adjusted","INTEGER NOT NULL DEFAULT 0"),
        ):
            if column not in evidence_columns:
                conn.execute(f"ALTER TABLE installation_evidence ADD COLUMN {column} {definition}")
        building_columns={row["name"] for row in conn.execute("PRAGMA table_info(buildings)")}
        if "dwelling_units" not in building_columns:
            conn.execute("ALTER TABLE buildings ADD COLUMN dwelling_units INTEGER")
        case_columns={row["name"] for row in conn.execute("PRAGMA table_info(house_number_cases)")}
        for column in ("floors","dwelling_units"):
            if column not in case_columns:
                conn.execute(f"ALTER TABLE house_number_cases ADD COLUMN {column} INTEGER")
        if "parcel_id" not in case_columns:
            conn.execute("ALTER TABLE house_number_cases ADD COLUMN parcel_id TEXT")
        if "street_side" not in case_columns:
            conn.execute("ALTER TABLE house_number_cases ADD COLUMN street_side TEXT NOT NULL DEFAULT 'UNDETERMINED'")
        catalog_columns={row["name"] for row in conn.execute("PRAGMA table_info(building_catalog)")}
        for column,definition in (
            ("admin_unit_id","TEXT REFERENCES admin_units(id)"),
            ("parcel_id","TEXT REFERENCES parcels(id)"),
            ("object_number","TEXT"),
            ("created_by","TEXT REFERENCES users(id)"),
            ("created_at","TEXT"),
        ):
            if column not in catalog_columns:
                conn.execute(f"ALTER TABLE building_catalog ADD COLUMN {column} {definition}")
        conn.execute("""CREATE UNIQUE INDEX IF NOT EXISTS ux_building_object_number
            ON building_catalog(admin_unit_id,object_number)
            WHERE admin_unit_id IS NOT NULL AND object_number IS NOT NULL""")
        defaults={
            "default_language":"ar","citizen_search_enabled":"true",
            "citizen_pdf_enabled":"true","support_email":"support@address.gov.sy",
            "map_default_layer":"satellite","zabadani_roads_enabled":"true"
        }
        for key,value in defaults.items():
            conn.execute("INSERT OR IGNORE INTO system_settings VALUES(?,?,NULL,?)",(key,value,now()))
        if conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]:
            # Local pilot migration v0.2: retain existing records while moving
            # the original four-digit demonstration code to the six-digit scheme.
            conn.execute("UPDATE addresses SET postal_code='010101' WHERE postal_code='0100'")
            if not conn.execute("SELECT COUNT(*) c FROM staff_profiles").fetchone()["c"]:
                conn.executemany("INSERT OR IGNORE INTO staff_profiles VALUES(?,?,?,?,1)",[
                    ("usr-editor","MUNICIPAL_EDITOR","Damascus Municipality","au-md"),
                    ("usr-reviewer","REVIEWER","Damascus Address Office","au-md"),
                    ("usr-approver","APPROVER","National Address Authority","au-di"),
                    ("usr-auditor","AUDITOR","Independent Audit Office","au-di"),
                    ("usr-admin","SYSTEM_ADMIN","National Platform Operations","au-sy")])
            legacy_extras=[
                ("usr-surveyor","surveyor","Pilot Surveyor","EDITOR","Survey123!","SURVEYOR","Damascus Survey Office","au-md"),
                ("usr-print","printoffice","Pilot Print Officer","APPROVER","Print123!","PRINT_OFFICER","Damascus Municipality","au-md"),
                ("usr-installer","installer","Pilot Installation Team","EDITOR","Install123!","INSTALLER","Damascus Field Team","au-md"),
                ("usr-zab-editor","zabadani.editor","Al-Zabadani Municipal Editor","EDITOR","Zabadani123!","MUNICIPAL_EDITOR","Municipality of Al-Zabadani","au-zab"),
                ("usr-zab-surveyor","zabadani.surveyor","Al-Zabadani Surveyor","EDITOR","ZabSurvey123!","SURVEYOR","Al-Zabadani Municipality","au-zab"),
                ("usr-zab-reviewer","zabadani.reviewer","Al-Zabadani Reviewer","REVIEWER","ZabReview123!","REVIEWER","Rif Dimashq Address Office","au-zab"),
                ("usr-zab-approver","zabadani.approver","Al-Zabadani Approver","APPROVER","ZabApprove123!","APPROVER","Rif Dimashq Address Office","au-zab"),
                ("usr-zab-installer","zabadani.installer","Al-Zabadani Field Installation","EDITOR","ZabInstall123!","INSTALLER","Al-Zabadani Field Team","au-zab"),
                ("usr-zab-registry","zabadani.registry","Al-Zabadani Population Registry","AUDITOR","ZabRegistry123!","REGISTRY_OFFICER","Al-Zabadani Registration Office","au-zab"),
            ]
            conn.executemany("INSERT OR IGNORE INTO users VALUES(?,?,?,?,?,1)",[(i,u,n,r,password_hash(p)) for i,u,n,r,p,_,_,_ in legacy_extras])
            conn.executemany("INSERT OR IGNORE INTO staff_profiles VALUES(?,?,?,?,1)",[(i,op,org,unit) for i,_,_,_,_,op,org,unit in legacy_extras])
            conn.executemany("INSERT OR IGNORE INTO admin_units VALUES(?,?,?,?,?,?,?)",[
                ("au-rd","SY-RD","GOVERNORATE","au-sy","ريف دمشق","Rif Dimashq","ACTIVE"),
                ("au-za","SY-RD-ZA","DISTRICT","au-rd","منطقة الزبداني","Al-Zabadani District","ACTIVE"),
                ("au-zab","SY-RD-ZA-ZAB","MUNICIPALITY","au-za","الزبداني","Al-Zabadani","PILOT")])
            conn.execute("INSERT OR IGNORE INTO postal_areas VALUES(?,?,?,?,?,?,?)",
                ("020401","au-zab","الزبداني","Al-Zabadani","Al-Zabadani","DRAFT",now()))
            conn.executemany("INSERT OR IGNORE INTO staff_admin_scopes VALUES(?,?,1,?)",[
                ("usr-zab-editor","au-zab",now()),("usr-zab-surveyor","au-zab",now()),
                ("usr-zab-reviewer","au-zab",now()),("usr-zab-approver","au-zab",now()),
                ("usr-zab-installer","au-zab",now()),("usr-zab-registry","au-zab",now())])
            seed_governorates(conn)
            sync_catalog(conn)
            return
        if APP_ENV=="production":
            admin_id="usr-"+uuid.uuid4().hex[:16]
            admin_username=os.getenv("SNA_BOOTSTRAP_ADMIN_USERNAME","state-admin")
            conn.executemany("INSERT INTO admin_units VALUES(?,?,?,?,?,?,?)",[
                ("au-sy","SY","COUNTRY",None,"الجمهورية العربية السورية","Syrian Arab Republic","ACTIVE"),
                ("au-rd","SY-RD","GOVERNORATE","au-sy","ريف دمشق","Rif Dimashq","ACTIVE"),
                ("au-za","SY-RD-ZA","DISTRICT","au-rd","منطقة الزبداني","Al-Zabadani District","ACTIVE"),
                ("au-zab","SY-RD-ZA-ZAB","MUNICIPALITY","au-za","الزبداني","Al-Zabadani","PILOT")])
            conn.execute("INSERT INTO users VALUES(?,?,?,?,?,1)",
                (admin_id,admin_username,"State Bootstrap Administrator","ADMIN",
                 secure_password_hash(os.environ["SNA_BOOTSTRAP_ADMIN_PASSWORD"])))
            conn.execute("INSERT INTO staff_profiles VALUES(?,?,?,?,1)",
                (admin_id,"SYSTEM_ADMIN","State Platform Operations","au-sy"))
            conn.execute("INSERT INTO staff_admin_scopes VALUES(?,?,1,?)",(admin_id,"au-sy",now()))
            audit(conn,admin_id,"BOOTSTRAP","system","production",None,{"environment":"production"})
            seed_governorates(conn)
            sync_catalog(conn)
            return
        users = [
            ("usr-editor", "editor", "Pilot Editor", "EDITOR", "Editor123!"),
            ("usr-reviewer", "reviewer", "Pilot Reviewer", "REVIEWER", "Review123!"),
            ("usr-approver", "approver", "Pilot Approver", "APPROVER", "Approve123!"),
            ("usr-auditor", "auditor", "Pilot Auditor", "AUDITOR", "Audit123!"),
            ("usr-admin", "admin", "Pilot Administrator", "ADMIN", "Admin123!"),
        ]
        conn.executemany("INSERT INTO users VALUES(?,?,?,?,?,1)",
                         [(i,u,n,r,password_hash(p)) for i,u,n,r,p in users])
        conn.executemany("INSERT INTO staff_profiles VALUES(?,?,?,?,1)",[
            ("usr-editor","MUNICIPAL_EDITOR","Damascus Municipality","au-md"),
            ("usr-reviewer","REVIEWER","Damascus Address Office","au-md"),
            ("usr-approver","APPROVER","National Address Authority","au-di"),
            ("usr-auditor","AUDITOR","Independent Audit Office","au-di"),
            ("usr-admin","SYSTEM_ADMIN","National Platform Operations","au-sy")])
        extra_users=[
            ("usr-surveyor","surveyor","Pilot Surveyor","EDITOR","Survey123!","SURVEYOR","Damascus Survey Office","au-md"),
            ("usr-print","printoffice","Pilot Print Officer","APPROVER","Print123!","PRINT_OFFICER","Damascus Municipality","au-md"),
            ("usr-installer","installer","Pilot Installation Team","EDITOR","Install123!","INSTALLER","Damascus Field Team","au-md"),
            ("usr-zab-editor","zabadani.editor","Al-Zabadani Municipal Editor","EDITOR","Zabadani123!","MUNICIPAL_EDITOR","Municipality of Al-Zabadani","au-zab"),
            ("usr-zab-surveyor","zabadani.surveyor","Al-Zabadani Surveyor","EDITOR","ZabSurvey123!","SURVEYOR","Al-Zabadani Municipality","au-zab"),
            ("usr-zab-reviewer","zabadani.reviewer","Al-Zabadani Reviewer","REVIEWER","ZabReview123!","REVIEWER","Rif Dimashq Address Office","au-zab"),
            ("usr-zab-approver","zabadani.approver","Al-Zabadani Approver","APPROVER","ZabApprove123!","APPROVER","Rif Dimashq Address Office","au-zab"),
            ("usr-zab-installer","zabadani.installer","Al-Zabadani Field Installation","EDITOR","ZabInstall123!","INSTALLER","Al-Zabadani Field Team","au-zab"),
            ("usr-zab-registry","zabadani.registry","Al-Zabadani Population Registry","AUDITOR","ZabRegistry123!","REGISTRY_OFFICER","Al-Zabadani Registration Office","au-zab"),
        ]
        conn.executemany("INSERT INTO users VALUES(?,?,?,?,?,1)",[(i,u,n,r,password_hash(p)) for i,u,n,r,p,_,_,_ in extra_users])
        conn.executemany("INSERT INTO staff_profiles VALUES(?,?,?,?,1)",[(i,op,org,unit) for i,_,_,_,_,op,org,unit in extra_users])
        conn.executemany("INSERT INTO admin_units VALUES(?,?,?,?,?,?,?)", [
            ("au-sy","SY","COUNTRY",None,"الجمهورية العربية السورية","Syrian Arab Republic","ACTIVE"),
            ("au-di","SY-DI","GOVERNORATE","au-sy","دمشق","Damascus","ACTIVE"),
            ("au-md","SY-DI-MD","MUNICIPALITY","au-di","مدينة دمشق","Damascus City","ACTIVE"),
            ("au-sh","SY-DI-MD-SH","DISTRICT","au-md","الشعلان","Al-Shaalan","ACTIVE"),
            ("au-rd","SY-RD","GOVERNORATE","au-sy","ريف دمشق","Rif Dimashq","ACTIVE"),
            ("au-za","SY-RD-ZA","DISTRICT","au-rd","منطقة الزبداني","Al-Zabadani District","ACTIVE"),
            ("au-zab","SY-RD-ZA-ZAB","MUNICIPALITY","au-za","الزبداني","Al-Zabadani","PILOT"),
        ])
        conn.execute("INSERT INTO postal_areas VALUES(?,?,?,?,?,?,?)",
            ("020401","au-zab","الزبداني","Al-Zabadani","Al-Zabadani","DRAFT",now()))
        conn.executemany("INSERT INTO staff_admin_scopes VALUES(?,?,1,?)",[
            ("usr-zab-editor","au-zab",now()),("usr-zab-surveyor","au-zab",now()),
            ("usr-zab-reviewer","au-zab",now()),("usr-zab-approver","au-zab",now()),
            ("usr-zab-installer","au-zab",now()),("usr-zab-registry","au-zab",now())])
        conn.execute("INSERT INTO streets VALUES(?,?,?,?,?,?,?)",
            ("str-sh-001","SY-DI-MD-STR-000001","au-sh","شارع الحمراء","Al-Hamra Street","[]","ACTIVE"))
        building_geo = {"type":"Polygon","coordinates":[[[36.2895,33.5166],[36.2898,33.5166],[36.2898,33.5168],[36.2895,33.5168],[36.2895,33.5166]]]}
        conn.execute("INSERT INTO buildings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("bld-001","SY-DI-MD-BLD-000001","au-sh",json.dumps(building_geo),"RESIDENTIAL_MIXED",
             "EXISTING",4,12,"C","ORTHOPHOTO","2026-01-01",None,1))
        conn.execute("INSERT INTO addresses VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("adr-001","SY-DI-MD-ADR-000001","str-sh-001","bld-001","12","010101","A",
             "شارع الحمراء ١٢، الشعلان، دمشق","12 Al-Hamra Street, Al-Shaalan, Damascus",
             36.28964,33.51669,"C","OFFICIAL","2026-01-01",None,1))
        audit(conn, "usr-admin", "SEED", "system", "pilot", None, {"dataset":"Damascus pilot"})
        seed_governorates(conn)
        sync_catalog(conn)

def encode_token(user):
    operational_role = user["operational_role"] if "operational_role" in user.keys() else user["role"]
    payload = f"{user['id']}|{operational_role}|{int(time.time()) + TOKEN_TTL_SECONDS}"
    sig = hmac.new(TOKEN_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}|{sig}"

def decode_token(token):
    try:
        user_id, role, expiry, sig = token.split("|")
        payload = f"{user_id}|{role}|{expiry}"
        if int(expiry) < time.time() or not hmac.compare_digest(sig, hmac.new(TOKEN_SECRET, payload.encode(), hashlib.sha256).hexdigest()):
            return None
        return {"id": user_id, "role": role}
    except (ValueError, TypeError):
        return None

class Handler(BaseHTTPRequestHandler):
    server_version = "SNA-Production-Candidate/0.17"

    def log_message(self, fmt, *args):
        request_id=getattr(self,"request_id",None) or uuid.uuid4().hex
        print(json.dumps({"time":now(),"request_id":request_id,"remote":self.client_address[0],
                          "message":fmt % args},ensure_ascii=False),flush=True)

    def security_headers(self, cache_control="no-store"):
        if not getattr(self,"request_id",None):self.request_id=uuid.uuid4().hex
        self.send_header("X-Request-ID",self.request_id)
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","DENY")
        self.send_header("X-Permitted-Cross-Domain-Policies","none")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Permissions-Policy","camera=(self), geolocation=(self), microphone=()")
        self.send_header("Cross-Origin-Opener-Policy","same-origin")
        self.send_header("Cross-Origin-Resource-Policy","same-origin")
        self.send_header("Cache-Control",cache_control)
        self.send_header("Content-Security-Policy","default-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; object-src 'none'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data: blob: https://tile.openstreetmap.org https://server.arcgisonline.com; connect-src 'self' https://tile.openstreetmap.org https://server.arcgisonline.com https://demotiles.maplibre.org")
        if APP_ENV=="production":self.send_header("Strict-Transport-Security","max-age=31536000; includeSubDomains")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        for key, val in JSON_HEADERS.items(): self.send_header(key, val)
        self.send_header("Content-Length", str(len(body)))
        self.security_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path):
        if not path.exists() or not path.is_file():
            return self.send_error(404)
        mime = {".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"application/javascript; charset=utf-8",".svg":"image/svg+xml"}.get(path.suffix,"application/octet-stream")
        data = path.read_bytes()
        self.send_response(200); self.send_header("Content-Type",mime); self.send_header("Content-Length",str(len(data)))
        self.security_headers("public, max-age=3600" if path.suffix not in (".html",) else "no-store")
        self.end_headers(); self.wfile.write(data)

    def send_pdf(self,data,filename):
        self.send_response(200);self.send_header("Content-Type","application/pdf")
        self.send_header("Content-Disposition",f'attachment; filename="{filename}"')
        self.send_header("Content-Length",str(len(data)));self.security_headers()
        self.end_headers();self.wfile.write(data)

    def send_attachment(self,data,filename,content_type):
        if isinstance(data,str):data=data.encode("utf-8")
        self.send_response(200);self.send_header("Content-Type",content_type)
        self.send_header("Content-Disposition",f'attachment; filename="{filename}"')
        self.send_header("Content-Length",str(len(data)));self.security_headers()
        self.end_headers();self.wfile.write(data)

    def body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 5_000_000: raise ValueError("request too large")
        return json.loads(self.rfile.read(length) or b"{}")

    def actor(self):
        auth = self.headers.get("Authorization","")
        return decode_token(auth[7:]) if auth.startswith("Bearer ") else None

    def require(self, roles):
        actor = self.actor()
        if not actor: self.send_json({"error":"authentication_required"},401); return None
        if actor["role"] not in roles: self.send_json({"error":"forbidden"},403); return None
        with db() as conn:
            profile=conn.execute("""SELECT p.organisation,p.admin_unit_id FROM staff_profiles p
                JOIN users u ON u.id=p.user_id
                WHERE p.user_id=? AND p.active=1 AND u.active=1""",(actor["id"],)).fetchone()
        if not profile:self.send_json({"error":"account_inactive"},401);return None
        REQUEST_CONTEXT.value={
            "request_id":getattr(self,"request_id",None),
            "server_time":now(),"remote_address":self.client_address[0],
            "user_agent":self.headers.get("User-Agent","")[:300],
            "device_time":self.headers.get("X-Device-Time"),
            "actor_role":actor["role"],
            "organisation":profile["organisation"] if profile else None,
            "admin_unit_id":profile["admin_unit_id"] if profile else None
        }
        return actor

    def data_scope(self,actor,requested=None,allow_national=False):
        """Resolve and enforce the administrative data partition for this request."""
        requested=(requested or "").strip()
        with db() as conn:
            if actor["role"]=="SYSTEM_ADMIN":
                if requested=="ALL" and allow_national:return "ALL"
                if not requested:return PILOT_UNIT_ID
                row=conn.execute("SELECT id FROM admin_units WHERE id=? AND level='GOVERNORATE' AND status='ACTIVE'",(requested,)).fetchone()
                if row:return row["id"]
                self.send_json({"error":"invalid_administrative_scope"},422);return None
            governorate=assigned_governorate(conn,actor["id"])
            profile=conn.execute("SELECT admin_unit_id FROM staff_profiles WHERE user_id=? AND active=1",(actor["id"],)).fetchone()
            scope=governorate if actor["role"]=="GOVERNORATE_ADMIN" else (profile["admin_unit_id"] if profile else None)
            if not scope:
                self.send_json({"error":"administrative_scope_missing"},403);return None
            if requested and requested not in {scope,governorate}:
                self.send_json({"error":"outside_assigned_governorate"},403);return None
            return scope

    def valid_host(self):
        host=self.headers.get("Host","").split(":",1)[0].lower()
        if host not in ALLOWED_HOSTS:
            self.send_json({"error":"invalid_host"},400)
            return False
        return True

    def do_GET(self):
        if not self.valid_host():return
        parsed = urlparse(self.path); path = parsed.path
        if path in ("/","/admin"): return self.send_file(STATIC / ("admin.html" if path == "/admin" else "index.html"))
        if path.startswith("/static/"):
            safe = (STATIC / path.removeprefix("/static/")).resolve()
            return self.send_file(safe) if STATIC.resolve() in safe.parents else self.send_error(403)
        if path == "/health": return self.send_json({"status":"ok","service":"sna-production-candidate","version":"0.18.0"})
        if path == "/ready":
            checks={"database":False,"audit_chain":False,"national_catalog":NATIONAL_DB.exists(),
                    "boundary":(DATA/"syria_boundary.geojson").exists()}
            detail={}
            try:
                with db() as conn:
                    conn.execute("SELECT 1").fetchone()
                    checks["database"]=True
                    detail["audit"]=audit_chain_status(conn)
                    checks["audit_chain"]=detail["audit"]["valid"]
            except sqlite3.Error as exc:
                detail["database_error"]=str(exc)
            operational=all(checks.values())
            return self.send_json({"status":"operational" if operational else "unavailable",
                                   "production_authorized":False,"checks":checks,"detail":detail},
                                  200 if operational else 503)
        if path == "/api/v1/national/statistics":
            if not NATIONAL_DB.exists():return self.send_json({"status":"not_imported"},503)
            with national_db() as conn: metadata=dict(conn.execute("SELECT key,value FROM metadata"))
            return self.send_json(metadata)
        m=re.fullmatch(r"/api/v1/pdf/(ADDRESS|ROAD|BUILDING|CASE|SYRIA_ROAD|SYRIA_BUILDING|PLACE)/([^/]+)",path)
        if m:
            kind,obj_id=m.group(1),m.group(2);record=None
            if kind=="CASE":
                actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","AUDITOR","SYSTEM_ADMIN"})
                if not actor:return
                with db() as conn:
                    r=conn.execute("""SELECT c.*,requester.display_name requested_name,
                        reviewer.display_name reviewed_name,approver.display_name approved_name
                        FROM house_number_cases c
                        LEFT JOIN users requester ON requester.id=c.requested_by
                        LEFT JOIN users reviewer ON reviewer.id=c.reviewed_by
                        LEFT JOIN users approver ON approver.id=c.approved_by WHERE c.id=?""",(obj_id,)).fetchone()
                    evidence=conn.execute("""SELECT e.*,u.display_name installed_name
                        FROM installation_evidence e LEFT JOIN users u ON u.id=e.installed_by
                        WHERE e.house_number_case_id=?""",(obj_id,)).fetchone()
                    events=conn.execute("""SELECT event_time,actor_id,action,chain_hash FROM audit_log
                        WHERE object_type='house_number_case' AND object_id=? ORDER BY id""",(obj_id,)).fetchall()
                if r:
                    coordinates=(f"{evidence['entrance_latitude']:.7f}, {evidence['entrance_longitude']:.7f}"
                        if evidence and evidence["entrance_latitude"] is not None else f"{r['latitude']:.7f}, {r['longitude']:.7f}")
                    record={"object_type":"HOUSE_NUMBER_CASE","dossier_number":f"CASE-{r['id']}",
                      "technical_code":r["building_ref"],"label_ar":r["street_name_ar"],
                      "label_en":r["street_name_en"],"house_number":r["house_number"],
                      "postal_code":r["postal_code"],"locality":r["locality_en"],
                      "coordinates":coordinates,"quality_level":"FIELD_CAPTURE" if evidence else "DRAFT",
                      "official_status":r["status"],"source":"Municipal controlled workflow",
                      "details":[
                        ("Floors",r["floors"]),("Dwellings",r["dwelling_units"]),
                        ("Requested by",r["requested_name"]),("Created at",r["created_at"]),
                        ("Reviewed by",r["reviewed_name"]),("Approved by",r["approved_name"]),
                        ("Installed by",evidence["installed_name"] if evidence else None),
                        ("Device time",evidence["device_time"] if evidence else None),
                        ("Server time",evidence["server_time"] if evidence else None),
                        ("GPS accuracy (m)",evidence["gps_accuracy_m"] if evidence else None),
                      ],"audit_events":[dict(event) for event in events],
                      "verification_value":events[-1]["chain_hash"] if events else r["id"]}
            elif kind=="ADDRESS":
                with db() as conn:r=conn.execute("SELECT * FROM addresses WHERE id=?",(obj_id,)).fetchone()
                if r:record={"object_type":"ADDRESS","dossier_number":r["official_code"],"technical_code":r["official_code"],
                  "label_ar":r["name_ar"],"label_en":r["name_en"],"house_number":r["house_number"],"postal_code":r["postal_code"],
                  "locality":"Syria","coordinates":f"{r['latitude']:.6f}, {r['longitude']:.6f}","quality_level":r["quality_level"],
                  "official_status":r["official_status"],"source":"National address registry","verification_value":r["official_code"]}
            elif kind in ("ROAD","BUILDING"):
                table="road_catalog" if kind=="ROAD" else "building_catalog"
                with db() as conn:
                    r=conn.execute(f"SELECT * FROM {table} WHERE id=?",(obj_id,)).fetchone()
                    d=conn.execute("SELECT * FROM object_dossiers WHERE object_type=? AND object_ref=?",(kind,obj_id)).fetchone()
                if r:record={"object_type":kind,"dossier_number":d["dossier_number"] if d else obj_id,
                  "technical_code":r["technical_code"],"label_ar":r["name_ar"] if kind=="ROAD" else None,
                  "label_en":r["name_en"] if kind=="ROAD" else "Building object",
                  "coordinates":f"{r['latitude']:.6f}, {r['longitude']:.6f}" if kind=="BUILDING" else None,
                  "quality_level":r["quality_level"],"official_status":r["official_status"],"source":r["source"]}
            else:
                table={"SYRIA_ROAD":"roads","SYRIA_BUILDING":"buildings","PLACE":"places"}[kind]
                try:source_id=int(obj_id.removeprefix("osm-road-").removeprefix("osm-building-").removeprefix("osm-place-"))
                except ValueError:return self.send_json({"error":"invalid_id"},400)
                with national_db() as conn:r=conn.execute(f"SELECT * FROM {table} WHERE osm_id=?",(source_id,)).fetchone()
                if r:record={"object_type":kind,"dossier_number":r["technical_code"],"technical_code":r["technical_code"],
                  "label_ar":r["name_ar"] if "name_ar" in r.keys() else None,
                  "label_en":r["name_en"] if "name_en" in r.keys() else None,
                  "locality":r["name"] if "name" in r.keys() else None,"coordinates":f"{r['lat']:.6f}, {r['lon']:.6f}",
                  "quality_level":"D","official_status":r["source_status"],"source":"Geofabrik / OpenStreetMap contributors"}
            if not record:return self.send_json({"error":"not_found"},404)
            return self.send_pdf(build_pdf(record),f"{record['technical_code']}.pdf")
        if path == "/api/v1/map/zabadani/roads":
            with db() as conn:
                enabled=conn.execute("""SELECT setting_value FROM system_settings
                    WHERE setting_key='zabadani_roads_enabled'""").fetchone()
            if enabled and enabled["setting_value"].lower()!="true":
                return self.send_json({"type":"FeatureCollection","features":[]})
            road_file=PILOT_ROADS
            if not road_file.exists(): return self.send_json({"error":"dataset_not_loaded"},503)
            return self.send_json(json.loads(road_file.read_text(encoding="utf-8")))
        if path == "/api/v1/map/zabadani/buildings":
            building_file=PILOT_BUILDINGS
            if not building_file.exists(): return self.send_json({"error":"dataset_not_loaded"},503)
            return self.send_json(json.loads(building_file.read_text(encoding="utf-8")))
        if path == "/api/v1/map/cadastre/buildings":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            requested=parse_qs(parsed.query).get("admin_unit_id",[""])[0][:40]
            scope=self.data_scope(actor,requested)
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                rows=conn.execute(f"""SELECT b.*,p.parcel_number,s.section_number
                    FROM building_catalog b
                    LEFT JOIN parcels p ON p.id=b.parcel_id
                    LEFT JOIN cadastral_sections s ON s.id=p.cadastral_section_id
                    WHERE b.admin_unit_id IN ({marks})
                    ORDER BY CAST(b.object_number AS INTEGER),b.object_number""",units).fetchall()
            return self.send_json({"type":"FeatureCollection","features":[{
                "type":"Feature","id":row["id"],"geometry":json.loads(row["geometry_geojson"]),
                "properties":{"technical_code":row["technical_code"],"object_number":row["object_number"],
                    "centroid":[row["longitude"],row["latitude"]],"admin_unit_id":row["admin_unit_id"],
                    "parcel_id":row["parcel_id"],"parcel_number":row["parcel_number"],
                    "section_number":row["section_number"],"quality_level":row["quality_level"],
                    "official_status":row["official_status"],"source":row["source"]}}
                for row in rows]})
        if path == "/api/v1/map/zabadani/number-proposals":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            requested=parse_qs(parsed.query).get("admin_unit_id",[""])[0][:40]
            scope=self.data_scope(actor,requested)
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                rows=[]
                if PILOT_UNIT_ID in units:
                    rows.extend(conn.execute("""SELECT p.building_ref,p.house_number,p.side,p.status,
                        b.longitude,b.latitude FROM provisional_number_assignments p
                        JOIN building_catalog b ON b.id=p.building_ref ORDER BY p.building_ref""").fetchall())
                official=conn.execute(f"""SELECT c.building_ref,c.house_number,c.street_side side,c.status,
                    c.longitude,c.latitude FROM house_number_cases c JOIN building_catalog b
                    ON b.id=c.building_ref WHERE b.admin_unit_id IN ({marks})
                    AND c.status NOT IN ('CANCELLED','REJECTED') ORDER BY c.created_at""",units).fetchall()
                by_building={row["building_ref"]:row for row in rows}
                by_building.update({row["building_ref"]:row for row in official})
                rows=list(by_building.values())
            return self.send_json({"type":"FeatureCollection","features":[{
                "type":"Feature","id":row["building_ref"],
                "geometry":{"type":"Point","coordinates":[row["longitude"],row["latitude"]]},
                "properties":{"building_ref":row["building_ref"],"house_number":row["house_number"],
                              "side":row["side"],"status":row["status"]}} for row in rows]})
        if path == "/api/v1/map/zabadani/parcels":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            requested=parse_qs(parsed.query).get("admin_unit_id",[""])[0][:40]
            scope=self.data_scope(actor,requested)
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                rows=conn.execute(f"""SELECT p.*,s.section_number,d.district_code,d.name_ar district_name_ar,
                    d.admin_unit_id
                    FROM parcels p JOIN cadastral_sections s ON s.id=p.cadastral_section_id
                    JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                    WHERE d.admin_unit_id IN ({marks}) ORDER BY s.section_number,p.parcel_number""",units).fetchall()
            return self.send_json({"type":"FeatureCollection","official_data_loaded":bool(rows),
                "features":[{"type":"Feature","id":row["id"],
                    "geometry":json.loads(row["geometry_geojson"]),
                    "properties":{"parcel_number":row["parcel_number"],
                        "section_number":row["section_number"],
                        "district_code":row["district_code"],
                        "admin_unit_id":row["admin_unit_id"],
                        "district_name_ar":row["district_name_ar"],
                        "quality_level":row["quality_level"],
                        "official_status":row["official_status"]}} for row in rows]})
        if path == "/api/v1/map/cadastre/sections":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            requested=parse_qs(parsed.query).get("admin_unit_id",[""])[0][:40]
            scope=self.data_scope(actor,requested)
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                rows=conn.execute(f"""SELECT s.*,d.admin_unit_id,d.district_code
                    FROM cadastral_sections s JOIN cadastral_districts d
                    ON d.id=s.cadastral_district_id WHERE d.admin_unit_id IN ({marks})
                    AND s.geometry_geojson IS NOT NULL ORDER BY CAST(s.section_number AS INTEGER),s.section_number""",units).fetchall()
            return self.send_json({"type":"FeatureCollection","features":[{
                "type":"Feature","id":row["id"],"geometry":json.loads(row["geometry_geojson"]),
                "properties":{"section_number":row["section_number"],"name_ar":row["name_ar"],
                    "admin_unit_id":row["admin_unit_id"],"district_code":row["district_code"],
                    "official_status":row["official_status"]}} for row in rows]})
        if path == "/api/v1/cadastre/zabadani/sections":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            requested=parse_qs(parsed.query).get("admin_unit_id",[""])[0][:40]
            scope=self.data_scope(actor,requested)
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                rows=conn.execute(f"""SELECT s.id,s.section_number,s.name_ar,s.geometry_geojson,s.official_status,
                    count(p.id) parcel_count FROM cadastral_sections s
                    JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                    LEFT JOIN parcels p ON p.cadastral_section_id=s.id
                    WHERE d.admin_unit_id IN ({marks}) GROUP BY s.id
                    ORDER BY CAST(s.section_number AS INTEGER),s.section_number""",units).fetchall()
            return self.send_json([{**dict(row),"geometry":json.loads(row["geometry_geojson"])
                if row["geometry_geojson"] else None} for row in rows])
        if path == "/api/v1/cadastre/zabadani/next-numbers":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            query=parse_qs(parsed.query);section_number=query.get("section_number",[""])[0][:30]
            scope=self.data_scope(actor,query.get("admin_unit_id",[""])[0][:40])
            if not scope:return
            with db() as conn:
                units=scoped_admin_unit_ids(conn,scope);marks=",".join("?" for _ in units)
                next_section=conn.execute(f"""SELECT coalesce(max(CASE WHEN s.section_number GLOB '[0-9]*'
                    THEN CAST(s.section_number AS INTEGER) END),0)+1 value
                    FROM cadastral_sections s JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                    WHERE d.admin_unit_id IN ({marks})""",units).fetchone()["value"]
                next_parcel=1
                if section_number:
                    row=conn.execute(f"""SELECT coalesce(max(CASE WHEN p.parcel_number GLOB '[0-9]*'
                        THEN CAST(p.parcel_number AS INTEGER) END),0)+1 value FROM parcels p
                        JOIN cadastral_sections s ON s.id=p.cadastral_section_id
                        JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                        WHERE d.admin_unit_id IN ({marks}) AND s.section_number=?""",(*units,section_number)).fetchone()
                    next_parcel=row["value"]
                next_object=conn.execute(f"""SELECT coalesce(max(CASE WHEN b.object_number GLOB '[0-9]*'
                    THEN CAST(b.object_number AS INTEGER) END),0)+1 value FROM building_catalog b
                    WHERE b.admin_unit_id IN ({marks})""",units).fetchone()["value"]
            return self.send_json({"next_section_number":str(next_section),
                "section_number":section_number or None,"next_parcel_number":str(next_parcel),
                "next_object_number":str(next_object)})
        if path == "/api/v1/map/syria/boundary":
            boundary_file=DATA/"syria_boundary.geojson"
            if not boundary_file.exists():return self.send_json({"error":"boundary_not_loaded"},503)
            return self.send_json(json.loads(boundary_file.read_text(encoding="utf-8")))
        if path == "/api/v1/map/syria/governorates":
            return self.send_json({"type":"FeatureCollection","features":governorate_features(),
                "source":"geoBoundaries 2.0.0","license":"CC BY 4.0",
                "status":"REFERENCE_BOUNDARIES_NOT_YET_STATE_RATIFIED"})
        if path == "/api/v1/catalog/search":
            query_params=parse_qs(parsed.query)
            q=query_params.get("q",[""])[0][:100]
            governorate_id=query_params.get("governorate_id",[""])[0][:30]
            if governorate_id:
                actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER",
                                    "PRINT_OFFICER","INSTALLER","AUDITOR","SYSTEM_ADMIN"})
                if not actor:return
                with db() as conn:
                    assigned=None if actor["role"]=="SYSTEM_ADMIN" else assigned_governorate(conn,actor["id"])
                if assigned and governorate_id!=assigned:
                    return self.send_json({"error":"outside_assigned_governorate"},403)
            like=f"%{q}%"; items=[]
            with db() as conn:
                for r in conn.execute("""SELECT * FROM road_catalog WHERE technical_code LIKE ? OR coalesce(name_ar,'') LIKE ?
                    OR coalesce(name_en,'') LIKE ? OR aliases LIKE ? ORDER BY coalesce(name_ar,technical_code) LIMIT 100""",(like,like,like,like)):
                    items.append({"object_type":"ROAD","id":r["id"],"technical_code":r["technical_code"],
                      "label_ar":r["name_ar"] or r["technical_code"],"label_en":r["name_en"],
                      "quality_level":r["quality_level"],"official_status":r["official_status"]})
                for r in conn.execute("""SELECT * FROM building_catalog WHERE technical_code LIKE ? OR id LIKE ?
                    ORDER BY technical_code LIMIT 50""",(like,like)):
                    items.append({"object_type":"BUILDING","id":r["id"],"technical_code":r["technical_code"],
                      "label_ar":r["technical_code"],"label_en":"Building object","longitude":r["longitude"],"latitude":r["latitude"],
                      "quality_level":r["quality_level"],"official_status":r["official_status"]})
                for r in conn.execute("""SELECT * FROM addresses WHERE valid_to IS NULL AND
                    (name_ar LIKE ? OR name_en LIKE ? OR official_code LIKE ? OR postal_code LIKE ? OR house_number LIKE ?)
                    ORDER BY official_code LIMIT 50""",(like,like,like,like,like)):
                    items.append({"object_type":"ADDRESS","id":r["id"],"technical_code":r["official_code"],
                      "label_ar":r["name_ar"],"label_en":r["name_en"],"longitude":r["longitude"],"latitude":r["latitude"],
                      "house_number":r["house_number"],"postal_code":r["postal_code"],"quality_level":r["quality_level"],
                      "official_status":r["official_status"]})
            if q and NATIONAL_DB.exists():
                with national_db() as nconn:
                    for r in nconn.execute("""SELECT * FROM roads WHERE coalesce(name_ar,'') LIKE ? OR
                        coalesce(name_en,'') LIKE ? OR coalesce(name,'') LIKE ? OR ref LIKE ?
                        ORDER BY CASE WHEN name_ar=? OR name=? THEN 0 ELSE 1 END LIMIT 80""",
                        (like,like,like,like,q,q)):
                        items.append({"object_type":"SYRIA_ROAD","id":f"osm-road-{r['osm_id']}",
                          "technical_code":r["technical_code"],"label_ar":r["name_ar"] or r["name"] or r["technical_code"],
                          "label_en":r["name_en"],"longitude":r["lon"],"latitude":r["lat"],
                          "quality_level":"D","official_status":r["source_status"]})
                    for r in nconn.execute("""SELECT * FROM places WHERE coalesce(name_ar,'') LIKE ? OR
                        coalesce(name_en,'') LIKE ? OR coalesce(name,'') LIKE ? ORDER BY place_type LIMIT 40""",(like,like,like)):
                        items.append({"object_type":"PLACE","id":f"osm-place-{r['osm_id']}",
                          "technical_code":r["technical_code"],"label_ar":r["name_ar"] or r["name"] or r["technical_code"],
                          "label_en":r["name_en"],"longitude":r["lon"],"latitude":r["lat"],
                          "quality_level":"D","official_status":r["source_status"]})
                    if q.upper().startswith("SY-OSM-BLD-"):
                        for r in nconn.execute("SELECT * FROM buildings WHERE technical_code LIKE ? LIMIT 30",(q+"%",)):
                            items.append({"object_type":"SYRIA_BUILDING","id":f"osm-building-{r['osm_id']}",
                              "technical_code":r["technical_code"],"label_ar":r["technical_code"],"label_en":"Building object",
                              "longitude":r["lon"],"latitude":r["lat"],"quality_level":"D","official_status":r["source_status"]})
            if governorate_id:
                boundary=next((feature for feature in governorate_features()
                    if feature.get("id")==governorate_id),None)
                if not boundary:return self.send_json({"error":"governorate_not_found"},404)
                items=[item for item in items if isinstance(item.get("longitude"),(int,float))
                    and isinstance(item.get("latitude"),(int,float))
                    and point_in_geometry(item["longitude"],item["latitude"],boundary["geometry"])]
            return self.send_json({"query":q,"governorate_id":governorate_id or None,
                "scope_enforced":bool(governorate_id),"items":items[:150]})
        m=re.fullmatch(r"/api/v1/national/objects/(ROAD|BUILDING|PLACE)/(\d+)",path)
        if m and NATIONAL_DB.exists():
            table={"ROAD":"roads","BUILDING":"buildings","PLACE":"places"}[m.group(1)]
            with national_db() as conn: row=conn.execute(f"SELECT * FROM {table} WHERE osm_id=?",(int(m.group(2)),)).fetchone()
            return self.send_json({"object_type":m.group(1),"object":dict(row) if row else None,
              "source":"Geofabrik / OpenStreetMap contributors","license":"ODbL 1.0","official":False},200 if row else 404)
        m=re.fullmatch(r"/api/v1/objects/(ROAD|BUILDING)/([^/]+)",path)
        if m:
            table="road_catalog" if m.group(1)=="ROAD" else "building_catalog"
            with db() as conn:
                row=conn.execute(f"SELECT * FROM {table} WHERE id=?",(m.group(2),)).fetchone()
                dossier=conn.execute("SELECT * FROM object_dossiers WHERE object_type=? AND object_ref=?",(m.group(1),m.group(2))).fetchone()
                assignments=conn.execute("SELECT * FROM house_number_cases WHERE building_ref=? ORDER BY created_at DESC",(m.group(2),)).fetchall() if m.group(1)=="BUILDING" else []
            if not row:return self.send_json({"error":"not_found"},404)
            return self.send_json({"object":dict(row),"dossier":dict(dossier) if dossier else None,
                                   "house_number_cases":[dict(a) for a in assignments]})
        m=re.fullmatch(r"/api/v1/buildings/([^/]+)/units",path)
        if m:
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER",
                                "REGISTRY_OFFICER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                entrances=conn.execute("""SELECT * FROM building_entrances
                    WHERE building_ref=? ORDER BY entrance_label""",(m.group(1),)).fetchall()
                units=conn.execute("""SELECT u.*,e.entrance_label FROM residential_units u
                    LEFT JOIN building_entrances e ON e.id=u.entrance_id
                    WHERE u.building_ref=? ORDER BY coalesce(u.floor_label,''),u.unit_number""",
                    (m.group(1),)).fetchall()
            return self.send_json({"building_ref":m.group(1),"entrances":[dict(x) for x in entrances],
                                   "units":[dict(x) for x in units],
                                   "resident_data_separated":True})
        m=re.fullmatch(r"/api/v1/units/([^/]+)/residents",path)
        if m:
            actor=self.require({"REGISTRY_OFFICER","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                rows=conn.execute("""SELECT r.id registration_id,r.residence_type,r.move_in_date,
                    r.move_out_date,r.status,p.register_number,p.given_names,p.family_name,
                    p.birth_date,p.protection_flag
                    FROM resident_registrations r JOIN population_persons p ON p.id=r.person_id
                    WHERE r.unit_id=? AND r.status='ACTIVE' ORDER BY p.family_name,p.given_names""",
                    (m.group(1),)).fetchall()
                audit(conn,actor["id"],"READ_PROTECTED_REGISTER","RESIDENTIAL_UNIT",m.group(1),
                      None,{"records":len(rows),"purpose":"municipal_population_register"})
            return self.send_json({"unit_id":m.group(1),"classification":"STRICTLY_PROTECTED",
                                   "residents":[dict(x) for x in rows]})
        if path in ("/api/v1/exports/google-addresses.kml","/api/v1/exports/google-addresses.csv",
                    "/api/v1/exports/google-addresses/validation"):
            actor=self.require({"SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                rows=conn.execute("""SELECT a.*,c.street_name_ar,c.street_name_en,c.locality_ar,c.locality_en,
                    c.updated_at source_updated_at,u.name_en state_en,u.name_ar state_ar
                    FROM addresses a LEFT JOIN house_number_cases c
                    ON c.building_ref=a.building_id AND c.status='APPROVED'
                    LEFT JOIN buildings b ON b.id=a.building_id
                    LEFT JOIN admin_units u ON u.id=b.admin_unit_id
                    WHERE a.valid_to IS NULL AND a.official_status='OFFICIAL'
                    ORDER BY a.official_code""").fetchall()
            records=[];issues=[]
            for row in rows:
                street=(row["street_name_en"] or row["street_name_ar"] or "").strip()
                city=(row["locality_en"] or row["locality_ar"] or row["state_en"] or "").strip()
                state=(row["state_en"] or row["state_ar"] or city).strip()
                problems=[]
                if not row["house_number"]:problems.append("missing_house_number")
                if not street:problems.append("missing_street_name")
                if not city:problems.append("missing_city")
                if not row["postal_code"]:problems.append("missing_postal_code")
                if row["latitude"] is None or row["longitude"] is None or not (-90<=row["latitude"]<=90 and -180<=row["longitude"]<=180):
                    problems.append("invalid_coordinates")
                if problems:
                    issues.append({"address_id":row["official_code"],"issues":problems});continue
                full=f"{row['house_number']} {street}, {city}, {state}, {row['postal_code']}, Syria"
                records.append({"ID":row["official_code"],"ST_NUM":row["house_number"],"ST_NAME":street,
                    "CITY":city,"STATE":state,"ZIP":row["postal_code"],"CNT_NAME":"Syria",
                    "LAT":row["latitude"],"LON":row["longitude"],"FULL_AD":full,
                    "COUNTRY":"SY","QUALITY":row["quality_level"],"UPDATED_AT":row["source_updated_at"] or row["valid_from"]})
            if path.endswith("/validation"):
                return self.send_json({"dataset":"Syrian official address points","total_official":len(rows),
                    "eligible_for_export":len(records),"blocked":len(issues),"issues":issues[:100],
                    "contains_personal_data":False,"geometry":"POINT","crs":"EPSG:4326"})
            if path.endswith(".csv"):
                output=io.StringIO(newline="");fields=list(records[0]) if records else ["ID","ST_NUM","ST_NAME","CITY","STATE","ZIP","CNT_NAME","LAT","LON","FULL_AD","COUNTRY","QUALITY","UPDATED_AT"]
                writer=csv.DictWriter(output,fieldnames=fields,quoting=csv.QUOTE_ALL);writer.writeheader();writer.writerows(records)
                return self.send_attachment("\ufeff"+output.getvalue(),"syrian-official-addresses-google.csv","text/csv; charset=utf-8")
            placemarks=[]
            for record in records:
                fields="".join(f'<Data name="{xml_escape(str(key))}"><value>{xml_escape(str(value))}</value></Data>' for key,value in record.items())
                placemarks.append(f'<Placemark><name>{xml_escape(record["FULL_AD"])}</name><ExtendedData>{fields}</ExtendedData><Point><coordinates>{record["LON"]},{record["LAT"]},0</coordinates></Point></Placemark>')
            kml='<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Syrian Official Address Points</name>'+"".join(placemarks)+"</Document></kml>"
            return self.send_attachment(kml,"syrian-official-addresses-google.kml","application/vnd.google-earth.kml+xml; charset=utf-8")
        if path in ("/api/v1/exports/addresses.geojson","/api/v1/exports/google-content-partner.geojson"):
            with db() as conn: rows=conn.execute("SELECT * FROM addresses WHERE valid_to IS NULL AND official_status='OFFICIAL'").fetchall()
            return self.send_json({"type":"FeatureCollection","name":"Syrian official address export",
              "license":"Export rights and recipient terms must be approved by the registry owner.",
              "features":[{"type":"Feature","id":r["official_code"],"geometry":{"type":"Point","coordinates":[r["longitude"],r["latitude"]]},
                "properties":{"address_id":r["official_code"],"formatted_address_ar":r["name_ar"],
                  "formatted_address_en":r["name_en"],"house_number":r["house_number"],"postal_code":r["postal_code"],
                  "entrance":r["entrance_label"],"quality_level":r["quality_level"],"status":r["official_status"]}} for r in rows]})
        if path == "/api/v1/addresses":
            params=parse_qs(parsed.query); q=params.get("q",[""])[0][:100]
            status=params.get("status",[""])[0][:30]; postal=params.get("postal_code",[""])[0][:6]
            like = f"%{q}%"
            with db() as conn:
                rows = conn.execute("""SELECT a.*,s.name_ar street_ar,s.name_en street_en,
                    b.floors,b.dwelling_units
                    FROM addresses a LEFT JOIN streets s ON s.id=a.street_id
                    LEFT JOIN buildings b ON b.id=a.building_id
                    WHERE a.valid_to IS NULL AND (a.name_ar LIKE ? OR a.name_en LIKE ? OR a.official_code LIKE ? OR a.postal_code LIKE ?)
                    AND (?='' OR a.official_status=?) AND (?='' OR a.postal_code=?)
                    ORDER BY a.official_code LIMIT 50""",(like,like,like,like,status,status,postal,postal)).fetchall()
            return self.send_json({"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[r["longitude"],r["latitude"]]},
                "properties":{k:r[k] for k in ("id","official_code","name_ar","name_en","house_number","postal_code","entrance_label","quality_level","official_status","floors","dwelling_units")}} for r in rows]})
        m = re.fullmatch(r"/api/v1/addresses/([^/]+)",path)
        if m:
            with db() as conn: row=conn.execute("SELECT * FROM addresses WHERE id=?",(m.group(1),)).fetchone()
            return self.send_json(dict(row) if row else {"error":"not_found"},200 if row else 404)
        if path == "/api/v1/change-requests":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","PRINT_OFFICER","INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn: rows=conn.execute("SELECT * FROM change_requests ORDER BY created_at DESC").fetchall()
            return self.send_json([dict(r)|{"payload":json.loads(r["payload"])} for r in rows])
        if path == "/api/v1/audit":
            actor=self.require({"AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn: rows=conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 200").fetchall()
            return self.send_json([dict(r) for r in rows])
        if path == "/api/v1/field-jobs":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","PRINT_OFFICER","INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                rows=conn.execute("""SELECT j.*,a.official_code,a.name_ar,a.name_en,a.postal_code
                    FROM field_jobs j JOIN addresses a ON a.id=j.address_id ORDER BY j.created_at DESC""").fetchall()
            return self.send_json([dict(r)|{"payload":json.loads(r["payload"]),"evidence":json.loads(r["evidence"]) if r["evidence"] else None} for r in rows])
        if path == "/api/v1/house-number-cases":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn: rows=conn.execute("SELECT * FROM house_number_cases ORDER BY created_at DESC").fetchall()
            return self.send_json([dict(r) for r in rows])
        if path == "/api/v1/numbering/next-house-number":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","SYSTEM_ADMIN"})
            if not actor:return
            query=parse_qs(parsed.query)
            building_ref=query.get("building_ref",[""])[0][:120]
            street_name_ar=query.get("street_name_ar",[""])[0].strip()[:240]
            street_side=query.get("street_side",["UNDETERMINED"])[0].upper()
            if not building_ref or not street_name_ar:
                return self.send_json({"error":"building_and_street_required"},422)
            if street_side not in {"LEFT","RIGHT","UNDETERMINED"}:
                return self.send_json({"error":"invalid_street_side"},422)
            with db() as conn:
                building=conn.execute("SELECT * FROM building_catalog WHERE id=?",(building_ref,)).fetchone()
                if not building:return self.send_json({"error":"building_not_found"},404)
                if not building["parcel_id"]:
                    return self.send_json({"error":"building_must_be_linked_to_parcel"},422)
                building_scope=building["admin_unit_id"] or PILOT_UNIT_ID
                if actor["role"]!="SYSTEM_ADMIN":
                    assigned=conn.execute("SELECT admin_unit_id FROM staff_profiles WHERE user_id=?",(actor["id"],)).fetchone()
                    if not assigned or building_scope not in scoped_admin_unit_ids(conn,assigned["admin_unit_id"]):
                        return self.send_json({"error":"outside_assigned_area"},403)
                unit=conn.execute("SELECT name_ar,name_en FROM admin_units WHERE id=?",(building_scope,)).fetchone()
                rows=conn.execute("""SELECT house_number FROM house_number_cases
                    WHERE locality_ar=? AND trim(street_name_ar)=trim(?)
                    AND status NOT IN ('CANCELLED','REJECTED')""",
                    (unit["name_ar"],street_name_ar)).fetchall()
            used=[int(row["house_number"]) for row in rows if re.fullmatch(r"[0-9]+",str(row["house_number"]).strip())]
            if street_side=="LEFT":
                side_numbers=[value for value in used if value%2==1]
                suggested=max(side_numbers)+2 if side_numbers else 1
                rule="ODD"
            elif street_side=="RIGHT":
                side_numbers=[value for value in used if value%2==0]
                suggested=max(side_numbers)+2 if side_numbers else 2
                rule="EVEN"
            else:
                suggested=max(used)+1 if used else 1
                rule="SEQUENTIAL"
            return self.send_json({"building_ref":building_ref,"parcel_id":building["parcel_id"],
                "street_name_ar":street_name_ar,"street_side":street_side,
                "suggested_house_number":str(suggested),"numbering_rule":rule,
                "entrance_point_required":True})
        if path == "/api/v1/numbering/zabadani":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                batch=conn.execute("SELECT * FROM numbering_batches WHERE admin_unit_id=? ORDER BY created_at DESC LIMIT 1",(PILOT_UNIT_ID,)).fetchone()
                counts=conn.execute("""SELECT status,count(*) count FROM provisional_number_assignments
                    GROUP BY status ORDER BY status""").fetchall()
            return self.send_json({"batch":dict(batch) if batch else None,"counts":[dict(row) for row in counts]})
        m=re.fullmatch(r"/api/v1/numbering/proposal/([^/]+)",path)
        if m:
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","INSTALLER","REVIEWER","APPROVER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                row=conn.execute("""SELECT p.*,r.technical_code road_code,r.name_ar road_name_ar,
                    r.name_en road_name_en FROM provisional_number_assignments p
                    JOIN road_catalog r ON r.id=p.road_ref WHERE p.building_ref=?""",
                    (m.group(1),)).fetchone()
                case=conn.execute("""SELECT * FROM house_number_cases WHERE building_ref=?
                    AND status NOT IN ('CANCELLED','REJECTED') ORDER BY created_at DESC LIMIT 1""",
                    (m.group(1),)).fetchone()
                evidence=conn.execute("SELECT * FROM installation_evidence WHERE house_number_case_id=?",
                    (case["id"],)).fetchone() if case else None
            if not row:return self.send_json({"error":"proposal_not_found"},404)
            result=dict(row)|{
                "case_id":case["id"] if case else None,
                "case_status":case["status"] if case else "PROPOSED",
                "street_name_ar":case["street_name_ar"] if case else (row["road_name_ar"] or f"طريق غير مسمى {row['road_code']}"),
                "street_name_en":case["street_name_en"] if case else (row["road_name_en"] or f"Unnamed road {row['road_code']}"),
                "locality_ar":PILOT_LOCALITY_AR,"locality_en":PILOT_LOCALITY_EN,
                "postal_code":PILOT_POSTAL_CODE,"postal_label":f"{PILOT_POSTAL_CODE} {PILOT_LOCALITY_EN}",
                "installation_evidence":dict(evidence) if evidence else None}
            return self.send_json(result)
        if path == "/api/v1/admin/governorates":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER",
                                "PRINT_OFFICER","INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                rows=conn.execute("""SELECT id,code official_code,name_ar,name_en,status
                    FROM admin_units WHERE level='GOVERNORATE'
                    ORDER BY code""").fetchall()
                assigned=None if actor["role"]=="SYSTEM_ADMIN" else assigned_governorate(conn,actor["id"])
                if assigned:rows=[row for row in rows if row["id"]==assigned]
            locations={item[0]:{"longitude":item[4],"latitude":item[5],"zoom":item[6]}
                       for item in SYRIA_GOVERNORATES}
            return self.send_json([dict(row)|locations.get(row["id"],{}) for row in rows])
        if path == "/api/v1/postal-areas":
            with db() as conn:rows=conn.execute("""SELECT z.*,u.name_ar admin_name_ar,u.name_en admin_name_en
                FROM postal_areas z JOIN admin_units u ON u.id=z.admin_unit_id ORDER BY z.postal_code""").fetchall()
            return self.send_json([dict(row)|{"label":f"{row['postal_code']} {row['locality_en']}"} for row in rows])
        if path == "/api/v1/settings":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","PRINT_OFFICER",
                                "INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:rows=conn.execute("SELECT * FROM system_settings ORDER BY setting_key").fetchall()
            return self.send_json({row["setting_key"]:row["setting_value"] for row in rows})
        if path == "/api/v1/support-tickets":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","PRINT_OFFICER",
                                "INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                if actor["role"]=="SYSTEM_ADMIN":
                    rows=conn.execute("SELECT * FROM support_tickets ORDER BY created_at DESC LIMIT 100").fetchall()
                else:
                    rows=conn.execute("""SELECT * FROM support_tickets WHERE created_by=?
                        ORDER BY created_at DESC LIMIT 50""",(actor["id"],)).fetchall()
            return self.send_json([dict(row) for row in rows])
        return self.send_json({"error":"not_found"},404)

    def do_POST(self):
        if not self.valid_host():return
        self.request_id=getattr(self,"request_id",None) or uuid.uuid4().hex
        REQUEST_CONTEXT.value={"request_id":self.request_id,"server_time":now(),
            "remote_address":self.client_address[0],"user_agent":self.headers.get("User-Agent","")[:300],
            "device_time":self.headers.get("X-Device-Time")}
        path=urlparse(self.path).path
        try: data=self.body()
        except (ValueError,json.JSONDecodeError) as exc: return self.send_json({"error":"invalid_json","detail":str(exc)},400)
        if path == "/api/v1/auth/login":
            login_key=f"{self.client_address[0]}|{str(data.get('username','')).lower()}"
            if not login_allowed(login_key):
                return self.send_json({"error":"too_many_login_attempts","retry_after_seconds":LOGIN_WINDOW_SECONDS},429)
            with db() as conn: user=conn.execute("""SELECT u.*,coalesce(p.operational_role,u.role) operational_role,
                p.organisation,p.admin_unit_id FROM users u LEFT JOIN staff_profiles p ON p.user_id=u.id
                WHERE u.username=? AND u.active=1 AND coalesce(p.active,1)=1""",(data.get("username"),)).fetchone()
            if not user or not verify_password(user["password_hash"],data.get("password","")):
                login_failed(login_key)
                return self.send_json({"error":"invalid_credentials"},401)
            login_succeeded(login_key)
            return self.send_json({"token":encode_token(user),"user":{"id":user["id"],"display_name":user["display_name"],
                "role":user["operational_role"],"organisation":user["organisation"],"admin_unit_id":user["admin_unit_id"]}})
        if path == "/api/v1/settings":
            actor=self.require({"SYSTEM_ADMIN"})
            if not actor:return
            allowed={"default_language","citizen_search_enabled","citizen_pdf_enabled",
                     "support_email","map_default_layer"}
            values=data.get("settings") if isinstance(data.get("settings"),dict) else {}
            if not values or not set(values).issubset(allowed):
                return self.send_json({"error":"invalid_settings"},422)
            if values.get("default_language") not in (None,"ar","en","de"):
                return self.send_json({"error":"invalid_default_language"},422)
            if values.get("map_default_layer") not in (None,"street","satellite","3d"):
                return self.send_json({"error":"invalid_map_layer"},422)
            with db() as conn:
                for key,value in values.items():
                    conn.execute("""INSERT INTO system_settings VALUES(?,?,?,?)
                        ON CONFLICT(setting_key) DO UPDATE SET setting_value=excluded.setting_value,
                        updated_by=excluded.updated_by,updated_at=excluded.updated_at""",
                        (key,str(value).lower() if isinstance(value,bool) else str(value),actor["id"],now()))
                audit(conn,actor["id"],"UPDATE","system_settings","global",None,values)
            return self.send_json({"updated":sorted(values)})
        if path == "/api/v1/cadastre/zabadani/print":
            actor=self.require({"MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            image=str(data.get("map_image",""))
            if not image.startswith("data:image/jpeg;base64,") or len(image)>4_500_000:
                return self.send_json({"error":"valid_map_image_required"},422)
            if data.get("paper") not in {"A4","A3"} or data.get("orientation") not in {"portrait","landscape"}:
                return self.send_json({"error":"invalid_print_template"},422)
            data["created_at"]=now()
            with db() as conn:
                rows=conn.execute("""SELECT p.id,p.parcel_number,p.geometry_geojson,s.section_number,
                    p.quality_level,p.official_status FROM parcels p JOIN cadastral_sections s
                    ON s.id=p.cadastral_section_id JOIN cadastral_districts d
                    ON d.id=s.cadastral_district_id WHERE d.admin_unit_id='au-zab'""").fetchall()
                data["parcels"]=[{"id":row["id"],"parcel_number":row["parcel_number"],
                    "section_number":row["section_number"],"quality_level":row["quality_level"],
                    "official_status":row["official_status"],"geometry":json.loads(row["geometry_geojson"])}
                    for row in rows]
                data["roads"]=json.loads(PILOT_ROADS.read_text(encoding="utf-8")).get("features",[])
                data["buildings"]=json.loads(PILOT_BUILDINGS.read_text(encoding="utf-8")).get("features",[])
                audit(conn,actor["id"],"PRINT","cadastral_map","SY-RD-ZA",None,
                      {"paper":data["paper"],"orientation":data["orientation"],"scale":data.get("scale")})
            return self.send_pdf(build_cadastral_map_pdf(data),"Liegenschaftskarte-Al-Zabadani.pdf")
        if path == "/api/v1/cadastre/zabadani/sections":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            scope=self.data_scope(actor,str(data.get("admin_unit_id","")).strip()[:40])
            if not scope:return
            section_number=str(data.get("section_number","")).strip()[:30]
            if section_number and not re.fullmatch(r"[0-9A-Za-z\u0600-\u06ff._/-]+",section_number):
                return self.send_json({"error":"invalid_section_number"},422)
            geometry=data.get("geometry") if isinstance(data.get("geometry"),dict) else None
            geometry_json=None
            if geometry is not None:
                ring=geometry.get("coordinates",[[]])[0] if geometry.get("type")=="Polygon" else []
                if len(ring)<4 or ring[0]!=ring[-1] or not all(isinstance(point,list) and len(point)>=2 and
                    all(isinstance(value,(int,float)) for value in point[:2]) for point in ring):
                    return self.send_json({"error":"valid_closed_section_polygon_required"},422)
                geometry_json=json.dumps(geometry,separators=(",",":"))
            with db() as conn:
                unit=conn.execute("SELECT code,name_ar,name_en FROM admin_units WHERE id=?",(scope,)).fetchone()
            if not unit:return self.send_json({"error":"administrative_scope_not_found"},404)
            district_code=f"{unit['code']}-CAD";district_id="cd-"+uuid.uuid5(uuid.NAMESPACE_URL,district_code).hex[:20]
            section_id="cs-"+uuid.uuid5(uuid.NAMESPACE_URL,f"{district_code}/{section_number}").hex[:20]
            stamp=now()
            try:
                with db() as conn:
                    conn.execute("BEGIN IMMEDIATE")
                    if not section_number:
                        section_number=str(conn.execute("""SELECT coalesce(max(CASE WHEN s.section_number GLOB '[0-9]*'
                            THEN CAST(s.section_number AS INTEGER) END),0)+1 value
                            FROM cadastral_sections s JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                            WHERE d.admin_unit_id=?""",(scope,)).fetchone()["value"])
                        section_id="cs-"+uuid.uuid5(uuid.NAMESPACE_URL,f"{district_code}/{section_number}").hex[:20]
                    name_ar=str(data.get("name_ar") or f"قطاع {section_number}").strip()[:160]
                    conn.execute("""INSERT INTO cadastral_districts(id,admin_unit_id,district_code,name_ar,name_en,official_status)
                        VALUES(?,?,?,?,?,'DRAFT') ON CONFLICT(district_code) DO NOTHING""",
                        (district_id,scope,district_code,unit["name_ar"],unit["name_en"]))
                    district_id=conn.execute("SELECT id FROM cadastral_districts WHERE district_code=?",(district_code,)).fetchone()["id"]
                    conn.execute("""INSERT INTO cadastral_sections
                        (id,cadastral_district_id,section_number,name_ar,geometry_geojson,official_status)
                        VALUES(?,?,?,?,?,'DRAFT')""",(section_id,district_id,section_number,name_ar,geometry_json))
                    request_id=str(uuid.uuid4())
                    payload={"section_id":section_id,"section_number":section_number,
                        "name_ar":name_ar,"has_geometry":geometry_json is not None}
                    conn.execute("INSERT INTO change_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (request_id,"CADASTRAL_SECTION",section_id,"CREATE",json.dumps(payload,ensure_ascii=False),
                         str(data.get("reason") or f"Katasterflur {unit['name_en']}")[:500],"SUBMITTED",
                         actor["id"],None,None,stamp,stamp))
                    audit(conn,actor["id"],"CREATE","cadastral_section",section_id,None,
                        {**payload,"official_status":"DRAFT"})
            except sqlite3.IntegrityError:
                return self.send_json({"error":"section_number_exists"},409)
            return self.send_json({"id":section_id,"section_number":section_number,
                "name_ar":name_ar,"official_status":"DRAFT","change_request_id":request_id,
                "next_step":"CAPTURE_PARCELS"},201)
        m=re.fullmatch(r"/api/v1/cadastre/zabadani/sections/([^/]+)/(update|delete)",path)
        if m:
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                row=conn.execute("""SELECT s.*,d.admin_unit_id FROM cadastral_sections s JOIN cadastral_districts d
                    ON d.id=s.cadastral_district_id WHERE s.id=?""",(m.group(1),)).fetchone()
                if not row:return self.send_json({"error":"not_found"},404)
                if actor["role"]!="SYSTEM_ADMIN":
                    governorate=assigned_governorate(conn,actor["id"])
                    profile=conn.execute("SELECT admin_unit_id FROM staff_profiles WHERE user_id=?",(actor["id"],)).fetchone()
                    scope=governorate if actor["role"]=="GOVERNORATE_ADMIN" else profile["admin_unit_id"]
                    if row["admin_unit_id"] not in scoped_admin_unit_ids(conn,scope):
                        return self.send_json({"error":"outside_assigned_governorate"},403)
                if row["official_status"] not in {"DRAFT","REJECTED"} and actor["role"]!="SYSTEM_ADMIN":
                    return self.send_json({"error":"approved_section_requires_formal_change"},409)
                if m.group(2)=="delete":
                    parcels=conn.execute("SELECT id FROM parcels WHERE cadastral_section_id=?",(row["id"],)).fetchall()
                    count=len(parcels)
                    cascade=data.get("cascade") is True and data.get("confirmation")=="DELETE_SECTION_AND_PARCELS"
                    if count and (actor["role"]!="SYSTEM_ADMIN" or not cascade):
                        return self.send_json({"error":"section_contains_parcels","parcel_count":count,
                            "admin_confirmation_required":actor["role"]=="SYSTEM_ADMIN"},409)
                    parcel_ids=[item["id"] for item in parcels]
                    for parcel_id in parcel_ids:
                        conn.execute("UPDATE house_number_cases SET parcel_id=NULL WHERE parcel_id=?",(parcel_id,))
                        conn.execute("UPDATE building_catalog SET parcel_id=NULL WHERE parcel_id=?",(parcel_id,))
                        conn.execute("DELETE FROM parcel_building_links WHERE parcel_id=?",(parcel_id,))
                        conn.execute("DELETE FROM change_requests WHERE object_type='PARCEL' AND object_id=?",(parcel_id,))
                    conn.execute("DELETE FROM parcels WHERE cadastral_section_id=?",(row["id"],))
                    conn.execute("DELETE FROM change_requests WHERE object_type='CADASTRAL_SECTION' AND object_id=?",(row["id"],))
                    conn.execute("DELETE FROM cadastral_sections WHERE id=?",(row["id"],))
                    audit(conn,actor["id"],"DELETE_CASCADE" if count else "DELETE_DRAFT",
                        "cadastral_section",row["id"],dict(row),{"deleted":True,"deleted_parcels":count})
                    return self.send_json({"id":row["id"],"deleted":True,"deleted_parcels":count})
                section_number=str(data.get("section_number",row["section_number"])).strip()[:30]
                name_ar=str(data.get("name_ar",row["name_ar"] or "")).strip()[:160]
                if not section_number or not re.fullmatch(r"[0-9A-Za-z\u0600-\u06ff._/-]+",section_number):
                    return self.send_json({"error":"invalid_section_number"},422)
                geometry_json=row["geometry_geojson"]
                geometry=data.get("geometry") if isinstance(data.get("geometry"),dict) else None
                if geometry is not None:
                    ring=geometry.get("coordinates",[[]])[0] if geometry.get("type")=="Polygon" else []
                    if len(ring)<4 or ring[0]!=ring[-1]:
                        return self.send_json({"error":"valid_closed_section_polygon_required"},422)
                    parcels=conn.execute("SELECT id,geometry_geojson FROM parcels WHERE cadastral_section_id=?",(row["id"],)).fetchall()
                    outside=[]
                    for parcel in parcels:
                        parcel_ring=json.loads(parcel["geometry_geojson"]).get("coordinates",[[]])[0]
                        if any(not point_in_geometry(point[0],point[1],geometry) for point in parcel_ring[:-1]):outside.append(parcel["id"])
                    if outside:return self.send_json({"error":"section_boundary_would_exclude_parcels",
                        "parcel_ids":outside},422)
                    geometry_json=json.dumps(geometry,separators=(",",":"))
                try:
                    conn.execute("UPDATE cadastral_sections SET section_number=?,name_ar=?,geometry_geojson=?,official_status='DRAFT' WHERE id=?",
                        (section_number,name_ar,geometry_json,row["id"]))
                except sqlite3.IntegrityError:
                    return self.send_json({"error":"section_number_exists"},409)
                audit(conn,actor["id"],"UPDATE","cadastral_section",row["id"],dict(row),
                    {"section_number":section_number,"name_ar":name_ar,"geometry_changed":geometry is not None})
            return self.send_json({"id":m.group(1),"section_number":section_number,"name_ar":name_ar,
                "official_status":"DRAFT"})
        m=re.fullmatch(r"/api/v1/cadastre/zabadani/parcels/([^/]+)/(update|delete)",path)
        if m:
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                row=conn.execute("""SELECT p.*,s.section_number,d.admin_unit_id FROM parcels p
                    JOIN cadastral_sections s ON s.id=p.cadastral_section_id
                    JOIN cadastral_districts d ON d.id=s.cadastral_district_id
                    WHERE p.id=?""",(m.group(1),)).fetchone()
                if not row:return self.send_json({"error":"not_found"},404)
                if actor["role"]!="SYSTEM_ADMIN":
                    governorate=assigned_governorate(conn,actor["id"])
                    profile=conn.execute("SELECT admin_unit_id FROM staff_profiles WHERE user_id=?",(actor["id"],)).fetchone()
                    scope=governorate if actor["role"]=="GOVERNORATE_ADMIN" else profile["admin_unit_id"]
                    if row["admin_unit_id"] not in scoped_admin_unit_ids(conn,scope):
                        return self.send_json({"error":"outside_assigned_governorate"},403)
                if row["official_status"] not in {"DRAFT","REJECTED"}:
                    return self.send_json({"error":"approved_parcel_requires_formal_change"},409)
                if m.group(2)=="delete":
                    conn.execute("UPDATE house_number_cases SET parcel_id=NULL WHERE parcel_id=?",(row["id"],))
                    conn.execute("DELETE FROM parcel_building_links WHERE parcel_id=?",(row["id"],))
                    conn.execute("DELETE FROM change_requests WHERE object_type='PARCEL' AND object_id=?",(row["id"],))
                    conn.execute("DELETE FROM parcels WHERE id=?",(row["id"],))
                    audit(conn,actor["id"],"DELETE_DRAFT","parcel",row["id"],dict(row),None)
                    return self.send_json({"id":row["id"],"deleted":True})
                parcel_number=str(data.get("parcel_number",row["parcel_number"])).strip()[:50]
                quality=str(data.get("quality_level",row["quality_level"])).upper()
                geometry=data.get("geometry")
                if not parcel_number or quality not in {"A","B","C","D","E"}:
                    return self.send_json({"error":"invalid_parcel_properties"},422)
                geometry_json=row["geometry_geojson"]
                if geometry is not None:
                    ring=geometry.get("coordinates",[[]])[0] if isinstance(geometry,dict) else []
                    if geometry.get("type")!="Polygon" or len(ring)<4 or ring[0]!=ring[-1]:
                        return self.send_json({"error":"valid_polygon_required"},422)
                    geometry_json=json.dumps(geometry,separators=(",",":"))
                try:
                    conn.execute("""UPDATE parcels SET parcel_number=?,quality_level=?,geometry_geojson=?,
                        official_status='DRAFT' WHERE id=?""",(parcel_number,quality,geometry_json,row["id"]))
                except sqlite3.IntegrityError:
                    return self.send_json({"error":"parcel_number_exists_in_section"},409)
                audit(conn,actor["id"],"UPDATE_DRAFT","parcel",row["id"],dict(row),
                    {"parcel_number":parcel_number,"quality_level":quality})
            return self.send_json({"id":m.group(1),"parcel_number":parcel_number,
                "quality_level":quality,"official_status":"DRAFT"})
        if path == "/api/v1/cadastre/buildings/capture":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            scope=self.data_scope(actor,str(data.get("admin_unit_id","")).strip()[:40])
            if not scope:return
            parcel_id=str(data.get("parcel_id","")).strip()[:80]
            object_number=str(data.get("object_number","")).strip()[:40]
            quality=str(data.get("quality_level","D")).upper()
            geometry=data.get("geometry") if isinstance(data.get("geometry"),dict) else {}
            ring=geometry.get("coordinates",[[]])[0] if geometry.get("type")=="Polygon" else []
            if quality not in {"A","B","C","D","E"}:
                return self.send_json({"error":"invalid_quality_level"},422)
            if geometry.get("type")!="Polygon" or len(ring)<4 or ring[0]!=ring[-1]:
                return self.send_json({"error":"valid_closed_building_polygon_required"},422)
            if not all(isinstance(point,list) and len(point)>=2 and
                       all(isinstance(value,(int,float)) for value in point[:2]) for point in ring):
                return self.send_json({"error":"invalid_coordinate"},422)
            with db() as conn:
                unit=conn.execute("SELECT code,name_ar,name_en FROM admin_units WHERE id=?",(scope,)).fetchone()
                if not unit:return self.send_json({"error":"administrative_scope_not_found"},404)
                parcel=conn.execute("""SELECT p.id,p.geometry_geojson,d.admin_unit_id FROM parcels p
                    JOIN cadastral_sections s ON s.id=p.cadastral_section_id
                    JOIN cadastral_districts d ON d.id=s.cadastral_district_id WHERE p.id=?""",
                    (parcel_id,)).fetchone()
                if not parcel:return self.send_json({"error":"parcel_required"},422)
                if parcel["admin_unit_id"]!=scope:return self.send_json({"error":"parcel_outside_selected_area"},403)
                parcel_geometry=json.loads(parcel["geometry_geojson"])
                outside=[point for point in ring[:-1] if not point_in_geometry(point[0],point[1],parcel_geometry)]
                if outside:return self.send_json({"error":"building_must_be_inside_selected_parcel",
                    "outside_point_count":len(outside)},422)
                conn.execute("BEGIN IMMEDIATE")
                if not object_number:
                    object_number=str(conn.execute("""SELECT coalesce(max(CASE WHEN object_number GLOB '[0-9]*'
                        THEN CAST(object_number AS INTEGER) END),0)+1 value FROM building_catalog
                        WHERE admin_unit_id=?""",(scope,)).fetchone()["value"])
                center_points=ring[:-1] or ring
                longitude=sum(point[0] for point in center_points)/len(center_points)
                latitude=sum(point[1] for point in center_points)/len(center_points)
                building_id="bld-"+uuid.uuid4().hex[:20]
                technical_code=f"{unit['code']}-BLD-{int(object_number):06d}" if object_number.isdigit() else f"{unit['code']}-BLD-{object_number}"
                stamp=now()
                try:
                    conn.execute("""INSERT INTO building_catalog
                        (id,technical_code,geometry_geojson,longitude,latitude,source,quality_level,
                         official_status,admin_unit_id,parcel_id,object_number,created_by,created_at)
                        VALUES(?,?,?,?,?,?,?,'DRAFT',?,?,?,?,?)""",
                        (building_id,technical_code,json.dumps(geometry,separators=(",",":")),longitude,latitude,
                         "MUNICIPAL_MAP_CAPTURE",quality,scope,parcel_id,object_number,actor["id"],stamp))
                except sqlite3.IntegrityError:
                    return self.send_json({"error":"object_number_exists_in_administrative_area"},409)
                dossier=f"DOS-{technical_code}"
                conn.execute("INSERT INTO object_dossiers VALUES(?,?,?,?,?,?,?,?)",
                    (dossier,"BUILDING",building_id,scope,"OPEN",
                     json.dumps({"parcel_id":parcel_id,"object_number":object_number,"quality":quality}),stamp,stamp))
                request_id=str(uuid.uuid4())
                payload={"building_ref":building_id,"technical_code":technical_code,"object_number":object_number,
                         "parcel_id":parcel_id,"quality_level":quality}
                conn.execute("INSERT INTO change_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (request_id,"BUILDING",building_id,"CREATE",json.dumps(payload,ensure_ascii=False),
                     str(data.get("reason") or f"Kommunale Gebäudeerfassung {unit['name_en']}")[:500],
                     "SUBMITTED",actor["id"],None,None,stamp,stamp))
                audit(conn,actor["id"],"CAPTURE_DRAFT","building",building_id,None,payload)
            return self.send_json({"id":building_id,"technical_code":technical_code,
                "object_number":object_number,"parcel_id":parcel_id,"status":"DRAFT",
                "change_request_id":request_id,"next_step":"ASSIGN_ENTRANCE_AND_HOUSE_NUMBER"},201)
        if path == "/api/v1/support-tickets":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","PRINT_OFFICER",
                                "INSTALLER","AUDITOR","SYSTEM_ADMIN"})
            if not actor:return
            subject=str(data.get("subject","")).strip();message=str(data.get("message","")).strip()
            category=str(data.get("category","TECHNICAL")).upper()
            if not subject or not message or category not in {"TECHNICAL","DATA","ACCOUNT","OTHER"}:
                return self.send_json({"error":"invalid_support_ticket"},422)
            ticket_id="sup-"+uuid.uuid4().hex[:12];stamp=now()
            with db() as conn:
                conn.execute("INSERT INTO support_tickets VALUES(?,?,?,?,?,?,?,?)",
                    (ticket_id,category,subject[:160],message[:4000],"OPEN",actor["id"],stamp,stamp))
                audit(conn,actor["id"],"CREATE","support_ticket",ticket_id,None,{"category":category,"subject":subject})
            return self.send_json({"id":ticket_id,"status":"OPEN"},201)
        if path == "/api/v1/cadastre/zabadani/parcels/import":
            actor=self.require({"SYSTEM_ADMIN"})
            if not actor:return
            if data.get("type")!="FeatureCollection" or not isinstance(data.get("features"),list):
                return self.send_json({"error":"geojson_feature_collection_required"},422)
            if not data["features"] or len(data["features"])>5000:
                return self.send_json({"error":"invalid_feature_count","maximum":5000},422)
            district=data.get("cadastral_district") or {}
            district_code=str(district.get("code","SY-RD-ZA")).strip()[:40]
            district_name_ar=str(district.get("name_ar","الزبداني")).strip()[:160]
            district_name_en=str(district.get("name_en","Al-Zabadani")).strip()[:160]
            if not district_code or not district_name_ar:
                return self.send_json({"error":"invalid_cadastral_district"},422)
            prepared=[]
            for index,feature in enumerate(data["features"]):
                geometry=feature.get("geometry") if isinstance(feature,dict) else None
                properties=feature.get("properties",{}) if isinstance(feature,dict) else {}
                if not isinstance(properties,dict) or not isinstance(geometry,dict) or geometry.get("type") not in {"Polygon","MultiPolygon"}:
                    return self.send_json({"error":"invalid_parcel_geometry","feature_index":index},422)
                if not isinstance(geometry.get("coordinates"),list) or not geometry["coordinates"]:
                    return self.send_json({"error":"empty_parcel_geometry","feature_index":index},422)
                section=str(properties.get("section_number","")).strip()[:30]
                parcel=str(properties.get("parcel_number","")).strip()[:50]
                quality=str(properties.get("quality_level","D")).upper()
                if not section or not parcel or quality not in {"A","B","C","D","E"}:
                    return self.send_json({"error":"invalid_parcel_properties","feature_index":index},422)
                prepared.append((section,parcel,quality,geometry))
            district_id="cd-"+uuid.uuid5(uuid.NAMESPACE_URL,district_code).hex[:20]
            created=updated=0
            with db() as conn:
                conn.execute("""INSERT INTO cadastral_districts(id,admin_unit_id,district_code,name_ar,name_en,official_status)
                    VALUES(?,?,?,?,?,'DRAFT') ON CONFLICT(district_code) DO UPDATE SET
                    name_ar=excluded.name_ar,name_en=excluded.name_en""",
                    (district_id,"au-zab",district_code,district_name_ar,district_name_en))
                district_id=conn.execute("SELECT id FROM cadastral_districts WHERE district_code=?",(district_code,)).fetchone()["id"]
                for section_number,parcel_number,quality,geometry in prepared:
                    section_id="cs-"+uuid.uuid5(uuid.NAMESPACE_URL,f"{district_code}/{section_number}").hex[:20]
                    conn.execute("""INSERT INTO cadastral_sections(id,cadastral_district_id,section_number,name_ar,official_status)
                        VALUES(?,?,?,?,'DRAFT') ON CONFLICT(cadastral_district_id,section_number) DO NOTHING""",
                        (section_id,district_id,section_number,f"قطاع {section_number}"))
                    section_id=conn.execute("""SELECT id FROM cadastral_sections
                        WHERE cadastral_district_id=? AND section_number=?""",(district_id,section_number)).fetchone()["id"]
                    previous=conn.execute("""SELECT * FROM parcels WHERE cadastral_section_id=?
                        AND parcel_number=?""",(section_id,parcel_number)).fetchone()
                    geometry_json=json.dumps(geometry,ensure_ascii=False,separators=(",",":"))
                    if previous:
                        conn.execute("""UPDATE parcels SET geometry_geojson=?,quality_level=?,official_status='DRAFT'
                            WHERE id=?""",(geometry_json,quality,previous["id"]))
                        audit(conn,actor["id"],"IMPORT_UPDATE","parcel",previous["id"],dict(previous),
                              {"section_number":section_number,"parcel_number":parcel_number,"quality_level":quality,"official_status":"DRAFT"})
                        updated+=1
                    else:
                        parcel_id="par-"+uuid.uuid4().hex[:20]
                        conn.execute("INSERT INTO parcels VALUES(?,?,?,?,?,'DRAFT')",
                            (parcel_id,section_id,parcel_number,geometry_json,quality))
                        audit(conn,actor["id"],"IMPORT_CREATE","parcel",parcel_id,None,
                              {"section_number":section_number,"parcel_number":parcel_number,"quality_level":quality,"official_status":"DRAFT"})
                        created+=1
            return self.send_json({"district_code":district_code,"created":created,"updated":updated,
                "status":"DRAFT","next_step":"TOPOLOGY_AND_SURVEY_REVIEW"},201)
        if path == "/api/v1/cadastre/zabadani/parcels/capture":
            actor=self.require({"GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            scope=self.data_scope(actor,str(data.get("admin_unit_id","")).strip()[:40])
            if not scope:return
            geometry=data.get("geometry");section_number=str(data.get("section_number","")).strip()[:30]
            parcel_number=str(data.get("parcel_number","")).strip()[:50]
            quality_level=str(data.get("quality_level","D")).upper()
            coordinates=geometry.get("coordinates") if isinstance(geometry,dict) else None
            ring=coordinates[0] if isinstance(coordinates,list) and coordinates else None
            if not section_number:
                return self.send_json({"error":"section_number_required"},422)
            if quality_level not in {"A","B","C","D","E"}:
                return self.send_json({"error":"invalid_quality_level"},422)
            if not isinstance(geometry,dict) or geometry.get("type")!="Polygon" or not isinstance(ring,list) or len(ring)<4:
                return self.send_json({"error":"valid_polygon_required"},422)
            if ring[0]!=ring[-1]:
                return self.send_json({"error":"polygon_must_be_closed"},422)
            for point in ring:
                if not isinstance(point,list) or len(point)<2 or not all(isinstance(value,(int,float)) for value in point[:2]):
                    return self.send_json({"error":"invalid_coordinate"},422)
            with db() as conn:
                unit=conn.execute("SELECT code,name_ar,name_en FROM admin_units WHERE id=?",(scope,)).fetchone()
            if not unit:return self.send_json({"error":"administrative_scope_not_found"},404)
            district_code=f"{unit['code']}-CAD";district_id="cd-"+uuid.uuid5(uuid.NAMESPACE_URL,district_code).hex[:20]
            section_id="cs-"+uuid.uuid5(uuid.NAMESPACE_URL,f"{district_code}/{section_number}").hex[:20]
            parcel_id="par-"+uuid.uuid4().hex[:20];stamp=now()
            with db() as conn:
                conn.execute("BEGIN IMMEDIATE")
                conn.execute("""INSERT INTO cadastral_districts(id,admin_unit_id,district_code,name_ar,name_en,official_status)
                    VALUES(?,?,?,?,?,'DRAFT') ON CONFLICT(district_code) DO NOTHING""",
                    (district_id,scope,district_code,unit["name_ar"],unit["name_en"]))
                district_id=conn.execute("SELECT id FROM cadastral_districts WHERE district_code=?",(district_code,)).fetchone()["id"]
                conn.execute("""INSERT INTO cadastral_sections(id,cadastral_district_id,section_number,name_ar,official_status)
                    VALUES(?,?,?,?,'DRAFT') ON CONFLICT(cadastral_district_id,section_number) DO NOTHING""",
                    (section_id,district_id,section_number,f"قطاع {section_number}"))
                section_id=conn.execute("""SELECT id FROM cadastral_sections WHERE cadastral_district_id=?
                    AND section_number=?""",(district_id,section_number)).fetchone()["id"]
                section_geometry=conn.execute("SELECT geometry_geojson FROM cadastral_sections WHERE id=?",(section_id,)).fetchone()["geometry_geojson"]
                if section_geometry:
                    allowed=json.loads(section_geometry)
                    outside=[point for point in ring[:-1] if not point_in_geometry(point[0],point[1],allowed)]
                    if outside:return self.send_json({"error":"parcel_must_be_inside_selected_section",
                        "outside_point_count":len(outside)},422)
                if not parcel_number:
                    parcel_number=str(conn.execute("""SELECT coalesce(max(CASE WHEN parcel_number GLOB '[0-9]*'
                        THEN CAST(parcel_number AS INTEGER) END),0)+1 value
                        FROM parcels WHERE cadastral_section_id=?""",(section_id,)).fetchone()["value"])
                existing=conn.execute("""SELECT * FROM parcels WHERE cadastral_section_id=? AND parcel_number=?""",
                    (section_id,parcel_number)).fetchone()
                if existing:
                    if existing["official_status"] not in {"DRAFT","REJECTED"}:
                        return self.send_json({"error":"approved_parcel_requires_formal_change"},409)
                    before=dict(existing);geometry_json=json.dumps(geometry,separators=(",",":"))
                    conn.execute("""UPDATE parcels SET geometry_geojson=?,quality_level=?,official_status='DRAFT'
                        WHERE id=?""",(geometry_json,quality_level,existing["id"]))
                    request=conn.execute("""SELECT id FROM change_requests WHERE object_type='PARCEL'
                        AND object_id=? AND status IN ('SUBMITTED','REVIEWED') ORDER BY created_at DESC LIMIT 1""",
                        (existing["id"],)).fetchone()
                    if request:
                        request_id=request["id"]
                        conn.execute("""UPDATE change_requests SET status='SUBMITTED',reviewed_by=NULL,
                            approved_by=NULL,updated_at=? WHERE id=?""",(stamp,request_id))
                    else:
                        request_id=str(uuid.uuid4())
                        payload={"parcel_id":existing["id"],"district_code":district_code,
                            "section_number":section_number,"parcel_number":parcel_number,"quality_level":quality_level}
                        conn.execute("INSERT INTO change_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                            (request_id,"PARCEL",existing["id"],"UPDATE",json.dumps(payload,ensure_ascii=False),
                             str(data.get("reason","Korrektur der Flurstücksgrenze"))[:500],"SUBMITTED",
                             actor["id"],None,None,stamp,stamp))
                    audit(conn,actor["id"],"UPDATE_DRAFT_GEOMETRY","parcel",existing["id"],before,
                          {"section_number":section_number,"parcel_number":parcel_number,
                           "quality_level":quality_level,"official_status":"DRAFT"})
                    return self.send_json({"id":existing["id"],"change_request_id":request_id,
                        "status":"DRAFT","updated":True,"next_step":"REVIEW"},200)
                conn.execute("INSERT INTO parcels VALUES(?,?,?,?,?,'DRAFT')",
                    (parcel_id,section_id,parcel_number,json.dumps(geometry,separators=(",",":")),quality_level))
                request_id=str(uuid.uuid4())
                payload={"parcel_id":parcel_id,"district_code":district_code,"section_number":section_number,
                    "parcel_number":parcel_number,"quality_level":quality_level}
                conn.execute("INSERT INTO change_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (request_id,"PARCEL",parcel_id,"CREATE",json.dumps(payload,ensure_ascii=False),
                     str(data.get("reason",f"Katastererfassung {unit['name_en']}"))[:500],"SUBMITTED",
                     actor["id"],None,None,stamp,stamp))
                audit(conn,actor["id"],"CAPTURE_DRAFT","parcel",parcel_id,None,payload)
            return self.send_json({"id":parcel_id,"change_request_id":request_id,"status":"DRAFT",
                "next_step":"REVIEW"},201)
        if path == "/api/v1/change-requests":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","SYSTEM_ADMIN"})
            if not actor:return
            required={"object_type","operation","payload","reason"}
            if not required.issubset(data): return self.send_json({"error":"missing_fields","required":sorted(required)},422)
            cid=str(uuid.uuid4()); stamp=now()
            with db() as conn:
                conn.execute("INSERT INTO change_requests VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (cid,data["object_type"],data.get("object_id"),data["operation"],json.dumps(data["payload"],ensure_ascii=False),
                     data["reason"],"SUBMITTED",actor["id"],None,None,stamp,stamp))
                audit(conn,actor["id"],"SUBMIT","change_request",cid,None,data)
            return self.send_json({"id":cid,"status":"SUBMITTED"},201)
        m=re.fullmatch(r"/api/v1/change-requests/([^/]+)/(review|approve|reject)",path)
        if m:
            action=m.group(2); roles={"review":{"REVIEWER","SYSTEM_ADMIN"},"approve":{"APPROVER","SYSTEM_ADMIN"},"reject":{"REVIEWER","APPROVER","SYSTEM_ADMIN"}}[action]
            actor=self.require(roles)
            if not actor:return
            with db() as conn:
                row=conn.execute("SELECT * FROM change_requests WHERE id=?",(m.group(1),)).fetchone()
                if not row:return self.send_json({"error":"not_found"},404)
                allowed={"review":{"SUBMITTED"},"approve":{"REVIEWED"},"reject":{"SUBMITTED","REVIEWED"}}[action]
                if row["status"] not in allowed:return self.send_json({"error":"invalid_transition","current":row["status"]},409)
                status={"review":"REVIEWED","approve":"APPROVED","reject":"REJECTED"}[action]
                field="reviewed_by" if action in ("review","reject") else "approved_by"
                conn.execute(f"UPDATE change_requests SET status=?,{field}=?,updated_at=? WHERE id=?",(status,actor["id"],now(),m.group(1)))
                if row["object_type"]=="PARCEL" and row["object_id"]:
                    parcel_status={"review":"IN_REVIEW","approve":"APPROVED","reject":"REJECTED"}[action]
                    conn.execute("UPDATE parcels SET official_status=? WHERE id=?",(parcel_status,row["object_id"]))
                if row["object_type"]=="CADASTRAL_SECTION" and row["object_id"]:
                    section_status={"review":"IN_REVIEW","approve":"APPROVED","reject":"REJECTED"}[action]
                    conn.execute("UPDATE cadastral_sections SET official_status=? WHERE id=?",(section_status,row["object_id"]))
                audit(conn,actor["id"],action.upper(),"change_request",m.group(1),dict(row),{"status":status})
            return self.send_json({"id":m.group(1),"status":status})
        if path == "/api/v1/field-jobs":
            actor=self.require({"APPROVER","PRINT_OFFICER","SYSTEM_ADMIN"})
            if not actor:return
            if data.get("job_type") not in {"PLAN_EXPORT","NOTICE_LETTER","PLAQUE_PRODUCTION","PLAQUE_INSTALLATION"}:
                return self.send_json({"error":"invalid_job_type"},422)
            jid=str(uuid.uuid4()); stamp=now()
            with db() as conn:
                address=conn.execute("SELECT id FROM addresses WHERE id=?",(data.get("address_id"),)).fetchone()
                if not address:return self.send_json({"error":"address_not_found"},404)
                conn.execute("INSERT INTO field_jobs VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (jid,data["address_id"],data["job_type"],"CREATED",data.get("assigned_to"),actor["id"],
                     json.dumps(data.get("payload",{}),ensure_ascii=False),None,stamp,stamp))
                audit(conn,actor["id"],"CREATE","field_job",jid,None,data)
            return self.send_json({"id":jid,"status":"CREATED"},201)
        if path == "/api/v1/house-number-cases":
            actor=self.require({"MUNICIPAL_EDITOR","SURVEYOR","SYSTEM_ADMIN"})
            if not actor:return
            required={"building_ref","street_name_ar","house_number","postal_code"}
            if not required.issubset(data):return self.send_json({"error":"missing_fields","required":sorted(required)},422)
            if not re.fullmatch(r"[0-9]{6}",str(data["postal_code"])):return self.send_json({"error":"invalid_postal_code"},422)
            try:
                floors=int(data.get("floors") or 0); dwelling_units=int(data.get("dwelling_units") or 0)
            except (TypeError,ValueError):
                return self.send_json({"error":"invalid_building_counts"},422)
            if not (0<=floors<=200 and 0<=dwelling_units<=5000):
                return self.send_json({"error":"invalid_building_counts"},422)
            street_side=str(data.get("street_side") or "UNDETERMINED").upper()
            if street_side not in {"LEFT","RIGHT","UNDETERMINED"}:
                return self.send_json({"error":"invalid_street_side"},422)
            with db() as conn:
                catalog=conn.execute("SELECT * FROM building_catalog WHERE id=?",(data["building_ref"],)).fetchone()
                if not catalog:return self.send_json({"error":"building_not_found"},404)
                building_scope=catalog["admin_unit_id"] or PILOT_UNIT_ID
                if actor["role"]!="SYSTEM_ADMIN":
                    assigned=conn.execute("SELECT admin_unit_id FROM staff_profiles WHERE user_id=?",(actor["id"],)).fetchone()
                    if not assigned or building_scope not in scoped_admin_unit_ids(conn,assigned["admin_unit_id"]):
                        return self.send_json({"error":"outside_assigned_area"},403)
                if catalog["admin_unit_id"] and not catalog["parcel_id"]:
                    return self.send_json({"error":"building_must_be_linked_to_parcel"},422)
                unit=conn.execute("SELECT name_ar,name_en FROM admin_units WHERE id=?",(building_scope,)).fetchone()
            building_lon,building_lat=catalog["longitude"],catalog["latitude"]
            if catalog["admin_unit_id"] and (data.get("entrance_longitude") is None or data.get("entrance_latitude") is None):
                return self.send_json({"error":"entrance_point_required"},422)
            try:
                lon=float(data.get("entrance_longitude",building_lon))
                lat=float(data.get("entrance_latitude",building_lat))
            except (TypeError,ValueError):
                return self.send_json({"error":"invalid_entrance_coordinates"},422)
            if not (-180<=lon<=180 and -90<=lat<=90):
                return self.send_json({"error":"invalid_entrance_coordinates"},422)
            rad=math.pi/180
            delta_lat=(lat-building_lat)*rad;delta_lon=(lon-building_lon)*rad
            hav=math.sin(delta_lat/2)**2+math.cos(building_lat*rad)*math.cos(lat*rad)*math.sin(delta_lon/2)**2
            entrance_distance_m=6371000*2*math.atan2(math.sqrt(hav),math.sqrt(max(0,1-hav)))
            if entrance_distance_m>150:
                return self.send_json({"error":"entrance_point_too_far_from_building",
                    "distance_m":round(entrance_distance_m,1),"maximum_m":150},422)
            parcel_id=data.get("parcel_id") or catalog["parcel_id"]
            if catalog["parcel_id"] and parcel_id!=catalog["parcel_id"]:
                return self.send_json({"error":"building_not_on_selected_parcel"},422)
            cid=str(uuid.uuid4()); stamp=now()
            try:
                with db() as conn:
                    duplicate=conn.execute("""SELECT id FROM house_number_cases
                        WHERE locality_ar=? AND trim(street_name_ar)=trim(?) AND house_number=?
                        AND postal_code=? AND status NOT IN ('CANCELLED','REJECTED') LIMIT 1""",
                        (unit["name_ar"],data["street_name_ar"],str(data["house_number"]),str(data["postal_code"]))).fetchone()
                    if duplicate:return self.send_json({"error":"house_number_exists_on_street","case_id":duplicate["id"]},409)
                    conn.execute("""INSERT INTO house_number_cases
                      (id,building_ref,locality_ar,locality_en,street_name_ar,street_name_en,
                       house_number,postal_code,longitude,latitude,status,requested_by,reviewed_by,
                       approved_by,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                      (cid,data["building_ref"],unit["name_ar"],unit["name_en"],data["street_name_ar"],data.get("street_name_en"),
                       str(data["house_number"]),str(data["postal_code"]),lon,lat,"SUBMITTED",actor["id"],None,None,stamp,stamp))
                    conn.execute("UPDATE house_number_cases SET floors=?,dwelling_units=? WHERE id=?",
                                 (floors,dwelling_units,cid))
                    conn.execute("UPDATE house_number_cases SET parcel_id=?,street_side=? WHERE id=?",
                                 (parcel_id,street_side,cid))
                    audit(conn,actor["id"],"SUBMIT","house_number_case",cid,None,{**data,
                        "entrance_longitude":lon,"entrance_latitude":lat,
                        "entrance_distance_m":round(entrance_distance_m,2)})
            except sqlite3.IntegrityError:return self.send_json({"error":"active_case_exists_for_building"},409)
            return self.send_json({"id":cid,"status":"SUBMITTED"},201)
        m=re.fullmatch(r"/api/v1/house-number-cases/([^/]+)/(update|cancel)",path)
        if m:
            action=m.group(2)
            actor=self.require({"MUNICIPAL_EDITOR","SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                case=conn.execute("SELECT * FROM house_number_cases WHERE id=?",(m.group(1),)).fetchone()
                if not case:return self.send_json({"error":"not_found"},404)
                if case["status"]!="SUBMITTED":
                    return self.send_json({"error":"official_or_processed_case_cannot_be_directly_changed",
                                           "current":case["status"]},409)
                if actor["role"]!="SYSTEM_ADMIN":
                    scope=conn.execute("""SELECT 1 FROM staff_admin_scopes
                        WHERE user_id=? AND admin_unit_id=? AND can_edit=1""",
                        (actor["id"],PILOT_UNIT_ID)).fetchone()
                    if not scope:return self.send_json({"error":"outside_assigned_area"},403)
                before=dict(case); stamp=now()
                if action=="cancel":
                    conn.execute("UPDATE house_number_cases SET status='CANCELLED',updated_at=? WHERE id=?",
                                 (stamp,m.group(1)))
                    conn.execute("""UPDATE provisional_number_assignments SET status='PROPOSED'
                        WHERE building_ref=?""",(case["building_ref"],))
                    after={"status":"CANCELLED","retained_for_audit":True}
                    audit(conn,actor["id"],"CANCEL","house_number_case",m.group(1),before,after)
                    return self.send_json({"id":m.group(1),"status":"CANCELLED",
                                           "deleted_from_active_work":True})
                house_number=str(data.get("house_number","")).strip()
                street_name_ar=str(data.get("street_name_ar","")).strip()
                street_name_en=str(data.get("street_name_en") or "").strip() or None
                postal_code=str(data.get("postal_code","")).strip()
                if not house_number or not street_name_ar:
                    return self.send_json({"error":"street_and_house_number_required"},422)
                if not re.fullmatch(r"[0-9]{6}",postal_code):
                    return self.send_json({"error":"invalid_postal_code"},422)
                try:
                    floors=int(data.get("floors",case["floors"] or 0))
                    dwelling_units=int(data.get("dwelling_units",case["dwelling_units"] or 0))
                except (TypeError,ValueError):
                    return self.send_json({"error":"invalid_building_counts"},422)
                if not (0<=floors<=200 and 0<=dwelling_units<=5000):
                    return self.send_json({"error":"invalid_building_counts"},422)
                conn.execute("""UPDATE house_number_cases SET street_name_ar=?,street_name_en=?,
                    house_number=?,postal_code=?,floors=?,dwelling_units=?,updated_at=? WHERE id=?""",
                    (street_name_ar,street_name_en,house_number,postal_code,floors,dwelling_units,stamp,m.group(1)))
                conn.execute("""UPDATE provisional_number_assignments SET house_number=?,status='MANUALLY_ADJUSTED'
                    WHERE building_ref=?""",(house_number,case["building_ref"]))
                after={"street_name_ar":street_name_ar,"street_name_en":street_name_en,
                       "house_number":house_number,"postal_code":postal_code,
                       "floors":floors,"dwelling_units":dwelling_units}
                audit(conn,actor["id"],"UPDATE","house_number_case",m.group(1),before,after)
            return self.send_json({"id":m.group(1),"status":"SUBMITTED","updated":True})
        m=re.fullmatch(r"/api/v1/house-number-cases/([^/]+)/install",path)
        if m:
            actor=self.require({"INSTALLER","SYSTEM_ADMIN"})
            if not actor:return
            evidence=data.get("evidence") if isinstance(data.get("evidence"),dict) else {}
            required={"latitude","longitude","device_time","plaque_installed","mailbox_installed",
                      "entrance_latitude","entrance_longitude","gps_accuracy_m"}
            if not required.issubset(evidence):return self.send_json({"error":"installation_evidence_required","required":sorted(required)},422)
            if evidence["plaque_installed"] is not True or evidence["mailbox_installed"] is not True:
                return self.send_json({"error":"plaque_and_mailbox_confirmation_required"},422)
            photo=evidence.get("photo_data")
            if photo and (not isinstance(photo,str) or len(photo)>700_000):
                return self.send_json({"error":"photo_too_large"},422)
            stamp=now();evidence_id="install-"+uuid.uuid4().hex[:12]
            try:
                with db() as conn:
                    case=conn.execute("SELECT * FROM house_number_cases WHERE id=?",(m.group(1),)).fetchone()
                    if not case:return self.send_json({"error":"not_found"},404)
                    if case["status"]!="SUBMITTED":return self.send_json({"error":"invalid_transition","current":case["status"]},409)
                    scope=conn.execute("""SELECT 1 FROM staff_admin_scopes WHERE user_id=? AND admin_unit_id=?
                        AND can_edit=1""",(actor["id"],PILOT_UNIT_ID)).fetchone()
                    if actor["role"]!="SYSTEM_ADMIN" and not scope:return self.send_json({"error":"outside_assigned_area"},403)
                    gps_lat=float(evidence["latitude"]); gps_lon=float(evidence["longitude"])
                    entrance_lat=float(evidence["entrance_latitude"]); entrance_lon=float(evidence["entrance_longitude"])
                    accuracy=max(0.0,float(evidence["gps_accuracy_m"]))
                    if not (-90<=gps_lat<=90 and -180<=gps_lon<=180 and
                            -90<=entrance_lat<=90 and -180<=entrance_lon<=180):
                        return self.send_json({"error":"invalid_coordinates"},422)
                    adjusted=1 if abs(gps_lat-entrance_lat)>0.000001 or abs(gps_lon-entrance_lon)>0.000001 else 0
                    conn.execute("""INSERT INTO installation_evidence
                        (id,house_number_case_id,installed_by,plaque_installed,mailbox_installed,
                         latitude,longitude,photo_data,device_time,server_time,verification_status,
                         gps_accuracy_m,entrance_latitude,entrance_longitude,entrance_adjusted)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (evidence_id,m.group(1),actor["id"],1,1,gps_lat,gps_lon,
                         photo,evidence["device_time"],stamp,"PENDING",accuracy,entrance_lat,entrance_lon,adjusted))
                    conn.execute("UPDATE house_number_cases SET status='INSTALLED',updated_at=? WHERE id=?",(stamp,m.group(1)))
                    audit(conn,actor["id"],"INSTALL","house_number_case",m.group(1),dict(case),
                        {"status":"INSTALLED","evidence_id":evidence_id})
            except sqlite3.IntegrityError:return self.send_json({"error":"installation_already_recorded"},409)
            return self.send_json({"id":m.group(1),"status":"INSTALLED","evidence_id":evidence_id})
        m=re.fullmatch(r"/api/v1/house-number-cases/([^/]+)/(review|approve|reject)",path)
        if m:
            action=m.group(2); roles={"review":{"REVIEWER","SYSTEM_ADMIN"},"approve":{"APPROVER","SYSTEM_ADMIN"},"reject":{"REVIEWER","APPROVER","SYSTEM_ADMIN"}}[action]
            actor=self.require(roles)
            if not actor:return
            with db() as conn:
                row=conn.execute("SELECT * FROM house_number_cases WHERE id=?",(m.group(1),)).fetchone()
                if not row:return self.send_json({"error":"not_found"},404)
                allowed={"review":{"SUBMITTED","INSTALLED"},"approve":{"REVIEWED"},"reject":{"SUBMITTED","INSTALLED","REVIEWED"}}[action]
                if row["status"] not in allowed:return self.send_json({"error":"invalid_transition","current":row["status"]},409)
                status={"review":"REVIEWED","approve":"APPROVED","reject":"REJECTED"}[action]
                field="reviewed_by" if action in ("review","reject") else "approved_by"
                conn.execute(f"UPDATE house_number_cases SET status=?,{field}=?,updated_at=? WHERE id=?",(status,actor["id"],now(),m.group(1)))
                if action=="approve":
                    bid=row["building_ref"]; aid="adr-"+uuid.uuid4().hex[:12]
                    installed=conn.execute("""SELECT entrance_longitude,entrance_latitude
                        FROM installation_evidence WHERE house_number_case_id=?""",(m.group(1),)).fetchone()
                    address_lon=installed["entrance_longitude"] if installed and installed["entrance_longitude"] is not None else row["longitude"]
                    address_lat=installed["entrance_latitude"] if installed and installed["entrance_latitude"] is not None else row["latitude"]
                    exists=conn.execute("SELECT id FROM buildings WHERE id=?",(bid,)).fetchone()
                    if not exists:
                        catalog=conn.execute("SELECT * FROM building_catalog WHERE id=?",(bid,)).fetchone()
                        if not catalog:return self.send_json({"error":"building_not_found"},404)
                        building_scope=catalog["admin_unit_id"] or PILOT_UNIT_ID
                        conn.execute("INSERT INTO buildings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                          (bid,catalog["technical_code"],building_scope,catalog["geometry_geojson"],"UNCLASSIFIED","EXISTING",row["floors"],row["dwelling_units"],catalog["quality_level"],catalog["source"],now(),None,1))
                    else:
                        conn.execute("UPDATE buildings SET floors=?,dwelling_units=?,version=version+1 WHERE id=?",
                          (row["floors"],row["dwelling_units"],bid))
                    if row["parcel_id"]:
                        conn.execute("""INSERT OR IGNORE INTO parcel_building_links
                            (parcel_id,building_ref,relation_type,valid_from,valid_to,created_by)
                            VALUES(?,?,'CONTAINS',?,NULL,?)""",
                            (row["parcel_id"],bid,now(),actor["id"]))
                    formatted_ar=f"{row['street_name_ar']} {row['house_number']}، {row['locality_ar']}، سوريا"
                    formatted_en=f"{row['house_number']} {row['street_name_en'] or row['street_name_ar']}, {row['locality_en']}, Syria"
                    conn.execute("INSERT INTO addresses VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (aid,f"SY-RD-ZA-ZAB-ADR-{aid[-12:].upper()}",None,bid,row["house_number"],row["postal_code"],"MAIN",
                       formatted_ar,formatted_en,address_lon,address_lat,"D","OFFICIAL",now(),None,1))
                    conn.execute("UPDATE provisional_number_assignments SET status='OFFICIAL' WHERE building_ref=?",(bid,))
                    conn.execute("UPDATE installation_evidence SET verification_status='VERIFIED' WHERE house_number_case_id=?",(m.group(1),))
                audit(conn,actor["id"],action.upper(),"house_number_case",m.group(1),dict(row),{"status":status})
            return self.send_json({"id":m.group(1),"status":status})
        m=re.fullmatch(r"/api/v1/staff/([^/]+)/deactivate",path)
        if m:
            actor=self.require({"SYSTEM_ADMIN"})
            if not actor:return
            with db() as conn:
                profile=conn.execute("SELECT * FROM staff_profiles WHERE user_id=?",(m.group(1),)).fetchone()
                if not profile:return self.send_json({"error":"not_found"},404)
                conn.execute("UPDATE staff_profiles SET active=0 WHERE user_id=?",(m.group(1),))
                conn.execute("UPDATE users SET active=0 WHERE id=?",(m.group(1),))
                audit(conn,actor["id"],"DEACTIVATE","staff",m.group(1),dict(profile),{"active":0})
            return self.send_json({"id":m.group(1),"active":False})
        m=re.fullmatch(r"/api/v1/field-jobs/([^/]+)/(print|produce|ready|install|verify)",path)
        if m:
            action=m.group(2)
            rules={
              "print":({"PRINT_OFFICER","SYSTEM_ADMIN"},{"CREATED"},"PRINTED"),
              "produce":({"PRINT_OFFICER","SYSTEM_ADMIN"},{"CREATED","PRINTED"},"IN_PRODUCTION"),
              "ready":({"PRINT_OFFICER","SYSTEM_ADMIN"},{"IN_PRODUCTION"},"READY"),
              "install":({"INSTALLER","SYSTEM_ADMIN"},{"READY","CREATED"},"INSTALLED"),
              "verify":({"MUNICIPAL_EDITOR","REVIEWER","SYSTEM_ADMIN"},{"INSTALLED"},"VERIFIED")}
            roles,allowed,status=rules[action]; actor=self.require(roles)
            if not actor:return
            with db() as conn:
                row=conn.execute("SELECT * FROM field_jobs WHERE id=?",(m.group(1),)).fetchone()
                if not row:return self.send_json({"error":"not_found"},404)
                if row["status"] not in allowed:return self.send_json({"error":"invalid_transition","current":row["status"]},409)
                evidence=data.get("evidence")
                if action=="install" and not isinstance(evidence,dict):
                    return self.send_json({"error":"installation_evidence_required"},422)
                conn.execute("UPDATE field_jobs SET status=?,assigned_to=coalesce(assigned_to,?),evidence=coalesce(?,evidence),updated_at=? WHERE id=?",
                    (status,actor["id"],json.dumps(evidence,ensure_ascii=False) if evidence else None,now(),m.group(1)))
                audit(conn,actor["id"],action.upper(),"field_job",m.group(1),dict(row),{"status":status,"evidence":evidence})
            return self.send_json({"id":m.group(1),"status":status})
        return self.send_json({"error":"not_found"},404)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--host",default="127.0.0.1"); parser.add_argument("--port",type=int,default=8080)
    parser.add_argument("--init-db",action="store_true"); parser.add_argument("--reset-db",action="store_true")
    args=parser.parse_args()
    problems=validate_production_config()
    if problems:
        raise SystemExit("Production configuration rejected:\n- "+"\n- ".join(problems))
    init_db(args.reset_db)
    if args.init_db: print(f"Initialized {DB_PATH}"); return
    print(f"SNA Pilot listening on http://{args.host}:{args.port}")
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()

if __name__ == "__main__": main()
