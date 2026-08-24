BEGIN;

CREATE TABLE sna.cadastral_district (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 official_code text UNIQUE NOT NULL,
 admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit,
 name_ar text NOT NULL,
 name_en text,
 valid_from timestamptz NOT NULL DEFAULT now(),
 valid_to timestamptz
);

CREATE TABLE sna.cadastral_section (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 cadastral_district_id uuid NOT NULL REFERENCES sna.cadastral_district,
 section_number text NOT NULL,
 name_ar text,
 geom geometry(MultiPolygon,4326) NOT NULL,
 area_m2 numeric GENERATED ALWAYS AS (ST_Area(geom::geography)) STORED,
 official_status sna.change_status NOT NULL DEFAULT 'DRAFT',
 valid_from timestamptz NOT NULL DEFAULT now(),
 valid_to timestamptz,
 UNIQUE(cadastral_district_id,section_number)
);

ALTER TABLE sna.parcel ADD COLUMN cadastral_section_id uuid REFERENCES sna.cadastral_section;
ALTER TABLE sna.parcel ADD CONSTRAINT parcel_number_unique_in_section
 UNIQUE(cadastral_section_id,cadastral_reference);
ALTER TABLE sna.building ADD COLUMN footprint_area_m2 numeric
 GENERATED ALWAYS AS (ST_Area(geom::geography)) STORED;

CREATE TABLE sna.parcel_ownership_record (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 parcel_id uuid NOT NULL REFERENCES sna.parcel,
 owner_name text NOT NULL,
 owner_reference text,
 share_percent numeric(7,4) NOT NULL DEFAULT 100,
 source_document text,
 status sna.change_status NOT NULL DEFAULT 'DRAFT',
 valid_from timestamptz NOT NULL DEFAULT now(),
 valid_to timestamptz,
 created_by uuid NOT NULL,
 CHECK(share_percent > 0 AND share_percent <= 100)
);

CREATE UNIQUE INDEX parcel_ownership_one_active_record
 ON sna.parcel_ownership_record(parcel_id) WHERE valid_to IS NULL;
CREATE INDEX cadastral_section_geom_gix ON sna.cadastral_section USING gist(geom);

REVOKE ALL ON sna.parcel_ownership_record FROM PUBLIC,sna_public,sna_editor;
GRANT SELECT ON sna.cadastral_district,sna.cadastral_section TO sna_editor,sna_reviewer,sna_approver,sna_auditor;
GRANT SELECT ON sna.parcel_ownership_record TO sna_reviewer,sna_approver,sna_auditor;

COMMENT ON TABLE sna.parcel_ownership_record IS
 'Protected internal register. Never expose through public address or map APIs.';
COMMENT ON COLUMN sna.cadastral_section.area_m2 IS
 'Computed capture area. It becomes authoritative only after survey approval.';

COMMIT;
