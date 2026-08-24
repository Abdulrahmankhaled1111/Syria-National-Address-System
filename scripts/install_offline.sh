#!/bin/sh
set -eu

test "$(id -u)" -ne 0 || { echo "Run as an unprivileged operations account, not root." >&2; exit 1; }
test -f SHA256SUMS.txt || { echo "SHA256SUMS.txt missing" >&2; exit 1; }
sha256sum -c SHA256SUMS.txt
test -f .env || { echo "Create .env from deploy/.env.offline.example and insert approved secrets." >&2; exit 1; }
test -f deploy/tls/fullchain.pem || { echo "Authority TLS certificate missing." >&2; exit 1; }
test -f deploy/tls/private-key.pem || { echo "Authority TLS private key missing." >&2; exit 1; }
docker load -i container-images.tar
docker compose --env-file .env -f docker-compose.offline.yml config >/dev/null
docker compose --env-file .env -f docker-compose.offline.yml up -d
docker compose --env-file .env -f docker-compose.offline.yml ps
