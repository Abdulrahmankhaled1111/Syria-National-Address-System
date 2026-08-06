"""Replace pilot logins with one national admin and 14 scoped governorate accounts."""
import argparse
import json
import secrets
import sqlite3
import string
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"app"))
from server import SYRIA_GOVERNORATES,audit,now,secure_password_hash

SLUGS={
    "au-di":"damascus","au-rd":"rif-dimashq","au-al":"aleppo","au-hi":"homs",
    "au-hm":"hama","au-la":"latakia","au-ta":"tartus","au-id":"idlib",
    "au-ra":"raqqa","au-dz":"deir-ez-zor","au-ha":"al-hasakah",
    "au-dr":"daraa","au-su":"as-suwayda","au-qu":"quneitra",
}

def temporary_password():
    alphabet=string.ascii_letters+string.digits+"!@#$%+-_"
    while True:
        value="".join(secrets.choice(alphabet) for _ in range(20))
        if any(c.islower() for c in value) and any(c.isupper() for c in value) and any(c.isdigit() for c in value):
            return value

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",required=True)
    parser.add_argument("--national-admin",default="admin")
    args=parser.parse_args()
    credentials=[]
    with sqlite3.connect(Path(args.db).resolve()) as connection:
        connection.row_factory=sqlite3.Row
        national=connection.execute("SELECT id FROM users WHERE username=? AND active=1",
                                    (args.national_admin,)).fetchone()
        if not national:raise SystemExit("active national administrator not found")
        before=connection.execute("SELECT count(*) count FROM users WHERE active=1 AND id<>?",
                                  (national["id"],)).fetchone()["count"]
        connection.execute("UPDATE users SET active=0 WHERE id<>?",(national["id"],))
        connection.execute("UPDATE staff_profiles SET active=0 WHERE user_id<>?",(national["id"],))
        for unit_id,code,name_ar,name_en,_,_,_ in SYRIA_GOVERNORATES:
            slug=SLUGS[unit_id]
            user_id=f"usr-gov-{slug}"
            username=f"gov.{slug}"
            password=temporary_password()
            display_name=f"{name_en} Governorate Administration"
            organisation=f"{name_en} Governorate"
            existing=connection.execute("SELECT id FROM users WHERE id=? OR username=?",
                                        (user_id,username)).fetchone()
            if existing:
                user_id=existing["id"]
                connection.execute("""UPDATE users SET username=?,display_name=?,role='EDITOR',
                    password_hash=?,active=1 WHERE id=?""",
                    (username,display_name,secure_password_hash(password),user_id))
            else:
                connection.execute("INSERT INTO users VALUES(?,?,?,?,?,1)",
                    (user_id,username,display_name,"EDITOR",secure_password_hash(password)))
            connection.execute("""INSERT INTO staff_profiles
                (user_id,operational_role,organisation,admin_unit_id,active)
                VALUES(?,?,?,?,1) ON CONFLICT(user_id) DO UPDATE SET
                operational_role=excluded.operational_role,organisation=excluded.organisation,
                admin_unit_id=excluded.admin_unit_id,active=1""",
                (user_id,"GOVERNORATE_ADMIN",organisation,unit_id))
            connection.execute("DELETE FROM staff_admin_scopes WHERE user_id=?",(user_id,))
            connection.execute("INSERT INTO staff_admin_scopes VALUES(?,?,1,?)",
                               (user_id,unit_id,now()))
            credentials.append({"code":code,"governorate":name_en,"username":username,
                                "temporary_password":password,"admin_unit_id":unit_id})
        audit(connection,national["id"],"REPLACE_PILOT_ACCOUNTS","staff","governorates",
              {"deactivated_accounts":before},{"active_governorate_accounts":14,
                                               "national_admin":args.national_admin})
    print(json.dumps({"national_admin":args.national_admin,
                      "governorate_accounts":credentials},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
