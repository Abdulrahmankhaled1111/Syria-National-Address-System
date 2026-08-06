"""Verify backup checksum and SQLite integrity without modifying it."""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("manifest")
    args=parser.parse_args()
    manifest_path=Path(args.manifest).resolve()
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    backup=manifest_path.parent/manifest["backup"]
    digest=hashlib.sha256(backup.read_bytes()).hexdigest()
    checksum_ok=digest==manifest["sha256"]
    with sqlite3.connect(f"file:{backup}?mode=ro",uri=True) as connection:
        integrity=connection.execute("PRAGMA integrity_check").fetchone()[0]
    result={"backup":str(backup),"checksum_ok":checksum_ok,"integrity":integrity,
            "ready":checksum_ok and integrity=="ok"}
    print(json.dumps(result))
    raise SystemExit(0 if result["ready"] else 2)


if __name__=="__main__":
    main()
