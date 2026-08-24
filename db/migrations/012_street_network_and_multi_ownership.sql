BEGIN;

ALTER TABLE sna.street ADD COLUMN IF NOT EXISTS source_name text;
ALTER TABLE sna.street ADD COLUMN IF NOT EXISTS imported_at timestamptz;
ALTER TABLE sna.parcel_ownership_record ADD COLUMN IF NOT EXISTS owner_address text;

DROP INDEX IF EXISTS sna.parcel_ownership_one_active_record;
CREATE INDEX IF NOT EXISTS parcel_ownership_active_records
 ON sna.parcel_ownership_record(parcel_id,valid_to);

COMMENT ON COLUMN sna.street.street_class IS
 'MOTORWAY, TRUNK, PRIMARY, SECONDARY, TERTIARY, LOCAL, SERVICE or PEDESTRIAN.';
COMMENT ON TABLE sna.parcel_ownership_record IS
 'Protected ownership register. Multiple active owners per parcel are allowed; shares must be verified against the source deed.';

COMMIT;
