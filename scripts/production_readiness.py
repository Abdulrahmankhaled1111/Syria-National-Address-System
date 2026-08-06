"""Fail closed when a deployment does not meet the production-candidate baseline."""
import argparse
import json
import os
import sqlite3
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",default="pilot.db")
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    failures=[]
    warnings=[]
    failures.append("application runtime still uses SQLite; PostgreSQL/PostGIS adapter is not active")
    secret=os.getenv("SNA_TOKEN_SECRET","")
    if len(secret)<32:failures.append("SNA_TOKEN_SECRET is missing or shorter than 32 characters")
    if os.getenv("SNA_ENV")!="production":failures.append("SNA_ENV is not production")
    if not os.getenv("SNA_ALLOWED_HOSTS"):failures.append("SNA_ALLOWED_HOSTS is missing")
    database=Path(args.db)
    if not database.exists():failures.append(f"database not found: {database}")
    else:
        with sqlite3.connect(database) as connection:
            demo=connection.execute("""SELECT count(*) FROM users WHERE username IN
                ('admin','editor','reviewer','approver','auditor','surveyor','installer')""").fetchone()[0]
            if demo:failures.append(f"{demo} documented demonstration accounts remain active")
            draft_postal=connection.execute("SELECT count(*) FROM postal_areas WHERE status!='OFFICIAL'").fetchone()[0]
            if draft_postal:failures.append(f"{draft_postal} postal areas are not official")
            unverified=connection.execute("SELECT count(*) FROM building_catalog WHERE official_status!='OFFICIAL'").fetchone()[0]
            if unverified:warnings.append(f"{unverified} building catalog objects remain unverified")
            pending=connection.execute("SELECT count(*) FROM house_number_cases WHERE status!='APPROVED'").fetchone()[0]
            if pending:warnings.append(f"{pending} house-number cases are not approved")
    result={"ready":not failures,"failures":failures,"warnings":warnings}
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["ready"] else 2)


if __name__=="__main__":
    main()
