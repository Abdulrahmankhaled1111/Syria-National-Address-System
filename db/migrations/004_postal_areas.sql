BEGIN;
CREATE TABLE sna.postal_area (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 postal_code varchar(6) UNIQUE NOT NULL CHECK (postal_code ~ '^[0-9]{6}$'),
 governorate_id uuid NOT NULL REFERENCES sna.admin_unit,
 name_ar text NOT NULL, name_en text, name_de text,
 geom geometry(MultiPolygon,4326) NOT NULL,
 status text NOT NULL DEFAULT 'ACTIVE',
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz,
 version integer NOT NULL DEFAULT 1
);
CREATE INDEX postal_area_geom_gix ON sna.postal_area USING gist(geom);
ALTER TABLE sna.address
  ADD CONSTRAINT address_postal_code_format
  CHECK (postal_code IS NULL OR postal_code ~ '^[0-9]{6}$');
GRANT SELECT ON sna.postal_area TO sna_public,sna_editor,sna_reviewer,sna_approver,sna_auditor;
COMMENT ON TABLE sna.postal_area IS 'Pilot proposal: postal delivery areas, independent of address and cadastral object identifiers';
COMMIT;
