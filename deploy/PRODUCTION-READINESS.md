# Production readiness gate

This repository is a production candidate, not an authorized state production
system. Deployment is prohibited until every blocking item below is closed and
signed by the responsible Syrian public authority.

## Technical gates

- Replace documented demonstration accounts and passwords.
- Replace the SQLite runtime with the reviewed PostgreSQL/PostGIS application
  adapter and test failover under load.
- Provide authority-issued TLS certificates and an approved DNS name.
- Connect the authority identity provider and enforce MFA for privileged roles.
- Move photo evidence to encrypted object storage with retention rules.
- Operate two separated application/database sites and an isolated immutable
  backup target.
- Complete restore, failover, penetration, dependency, and source-code reviews.
- Connect centralized monitoring, alerting, audit export, and incident response.

## Data and legal gates

- Approve the pilot boundary and responsible data-owning authority.
- Replace open map objects with surveyed or municipality-confirmed records.
- Approve the national identifier, address, and postal-code rules.
- Confirm the official national boundary dataset used by the state.
- Approve privacy notices, retention periods, access policy, and photo rules.
- Execute processor/operator agreements and an incident notification process.

## Mandatory checks

Run before every release:

```powershell
python -m unittest discover -s tests
python scripts/production_readiness.py --db pilot.db
docker compose -f docker-compose.production.yml config
```

The readiness script intentionally fails while demonstration accounts, draft
postal areas, or missing production secrets remain. A successful technical
check is necessary but does not replace state acceptance.
