"""Provision a named staff account without embedding credentials in source."""
import argparse
import getpass
import sqlite3
import sys
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"app"))
from server import SCHEMA,audit,now,secure_password_hash

ROLES={"MUNICIPAL_EDITOR":"EDITOR","SURVEYOR":"EDITOR","INSTALLER":"EDITOR",
       "REVIEWER":"REVIEWER","APPROVER":"APPROVER","PRINT_OFFICER":"APPROVER",
       "AUDITOR":"AUDITOR","GOVERNORATE_ADMIN":"EDITOR","SYSTEM_ADMIN":"ADMIN"}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",required=True)
    parser.add_argument("--username",required=True)
    parser.add_argument("--display-name",required=True)
    parser.add_argument("--operational-role",choices=sorted(ROLES),required=True)
    parser.add_argument("--organisation",required=True)
    parser.add_argument("--admin-unit",required=True)
    args=parser.parse_args()
    password=getpass.getpass("New account password: ")
    confirmation=getpass.getpass("Confirm password: ")
    if password!=confirmation:raise SystemExit("passwords do not match")
    if len(password)<14:raise SystemExit("password must contain at least 14 characters")
    user_id="usr-"+uuid.uuid4().hex[:16]
    with sqlite3.connect(Path(args.db).resolve()) as connection:
        connection.row_factory=sqlite3.Row
        connection.executescript(SCHEMA)
        if not connection.execute("SELECT 1 FROM admin_units WHERE id=?",(args.admin_unit,)).fetchone():
            raise SystemExit("admin unit does not exist")
        connection.execute("INSERT INTO users VALUES(?,?,?,?,?,1)",
            (user_id,args.username,args.display_name,ROLES[args.operational_role],secure_password_hash(password)))
        connection.execute("INSERT INTO staff_profiles VALUES(?,?,?,?,1)",
            (user_id,args.operational_role,args.organisation,args.admin_unit))
        connection.execute("INSERT INTO staff_admin_scopes VALUES(?,?,1,?)",
            (user_id,args.admin_unit,now()))
        audit(connection,None,"PROVISION","staff",user_id,None,
              {"username":args.username,"role":args.operational_role,"admin_unit":args.admin_unit})
    print(f"Created {user_id} for {args.username}")


if __name__=="__main__":
    main()
