#!/bin/sh
set -eu
if [ "$#" -ne 1 ]; then echo "Usage: restore.sh /backups/sna_TIMESTAMP.dump" >&2; exit 2; fi
backup="$1"
test -f "$backup"
test -f "${backup}.sha256"
(cd "$(dirname "$backup")" && sha256sum -c "$(basename "$backup").sha256")
echo "WARNING: restore replaces objects in database ${PGDATABASE:?} on ${PGHOST:?}."
test "${CONFIRM_RESTORE:-}" = "YES"
pg_restore --clean --if-exists --no-owner --dbname="$PGDATABASE" "$backup"
echo "Restore completed. Run application smoke tests now."
