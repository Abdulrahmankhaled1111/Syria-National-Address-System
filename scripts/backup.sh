#!/bin/sh
set -eu
umask 077
mkdir -p /backups
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
target="/backups/sna_${stamp}.dump"
pg_dump --format=custom --no-owner --file="$target"
sha256sum "$target" > "${target}.sha256"
pg_restore --list "$target" >/dev/null
echo "Backup created and verified: $target"
