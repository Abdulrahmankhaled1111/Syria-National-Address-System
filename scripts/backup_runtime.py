"""Create a consistent SQLite backup, checksum, and manifest."""
import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",required=True)
    parser.add_argument("--out-dir",required=True)
    args=parser.parse_args()
    source=Path(args.db).resolve()
    destination_dir=Path(args.out_dir).resolve()
    destination_dir.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination=destination_dir/f"registry-{stamp}.db"
    with sqlite3.connect(source) as source_db,sqlite3.connect(destination) as backup_db:
        source_db.backup(backup_db)
    digest=hashlib.sha256(destination.read_bytes()).hexdigest()
    manifest={"created_at":datetime.now(timezone.utc).isoformat(),"source":str(source),
              "backup":destination.name,"bytes":destination.stat().st_size,"sha256":digest}
    manifest_path=destination.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest))


if __name__=="__main__":
    main()
