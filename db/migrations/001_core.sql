BEGIN;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS sna;

CREATE TYPE sna.unit_level AS ENUM ('COUNTRY','GOVERNORATE','DISTRICT','SUBDISTRICT','MUNICIPALITY','LOCALITY','NEIGHBOURHOOD');
CREATE TYPE sna.quality_level AS ENUM ('A','B','C','D','E');
CREATE TYPE sna.lifecycle_status AS ENUM ('PLANNED','EXISTING','DAMAGED','DESTROYED','UNDER_RECONSTRUCTION','RETIRED');
CREATE TYPE sna.change_status AS ENUM ('DRAFT','SUBMITTED','REVIEWED','APPROVED','REJECTED','PUBLISHED','HISTORISED');

CREATE TABLE sna.admin_unit (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 level sna.unit_level NOT NULL, parent_id uuid REFERENCES sna.admin_unit,
 name_ar text NOT NULL, name_en text, name_ku text, alternative_names jsonb NOT NULL DEFAULT '[]',
 geom geometry(MultiPolygon,4326), valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz,
 version integer NOT NULL DEFAULT 1, CHECK(parent_id IS NULL OR parent_id <> id)
);
CREATE TABLE sna.street (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit, name_ar text NOT NULL, name_en text, name_ku text,
 former_names jsonb NOT NULL DEFAULT '[]', street_class text NOT NULL DEFAULT 'LOCAL',
 centreline geometry(MultiLineString,4326), lifecycle_status sna.lifecycle_status NOT NULL DEFAULT 'EXISTING',
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz, version integer NOT NULL DEFAULT 1
);
CREATE TABLE sna.parcel (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit, cadastral_reference text,
 geom geometry(MultiPolygon,4326) NOT NULL, area_m2 numeric GENERATED ALWAYS AS (ST_Area(geom::geography)) STORED,
 quality_level sna.quality_level NOT NULL, source_type text NOT NULL,
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz, version integer NOT NULL DEFAULT 1
);
CREATE TABLE sna.building (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit, geom geometry(MultiPolygon,4326) NOT NULL,
 function_code text NOT NULL, lifecycle_status sna.lifecycle_status NOT NULL, floors smallint,
 quality_level sna.quality_level NOT NULL, source_type text NOT NULL,
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz, version integer NOT NULL DEFAULT 1,
 CHECK(floors IS NULL OR floors BETWEEN 0 AND 200)
);
CREATE TABLE sna.parcel_building (
 parcel_id uuid REFERENCES sna.parcel, building_id uuid REFERENCES sna.building,
 relation_type text NOT NULL DEFAULT 'INTERSECTS', PRIMARY KEY(parcel_id,building_id)
);
CREATE TABLE sna.entrance (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 building_id uuid NOT NULL REFERENCES sna.building, label text, geom geometry(Point,4326) NOT NULL,
 accessible boolean, emergency_note text, quality_level sna.quality_level NOT NULL,
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz, version integer NOT NULL DEFAULT 1
);
CREATE TABLE sna.address (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), official_code text UNIQUE NOT NULL,
 street_id uuid REFERENCES sna.street, building_id uuid REFERENCES sna.building,
 entrance_id uuid REFERENCES sna.entrance, admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit,
 house_number text, postal_code text, formatted_ar text NOT NULL, formatted_en text, formatted_ku text,
 position geometry(Point,4326) NOT NULL, official_status text NOT NULL DEFAULT 'OFFICIAL',
 quality_level sna.quality_level NOT NULL, source_type text NOT NULL,
 valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz, version integer NOT NULL DEFAULT 1,
 CHECK(street_id IS NOT NULL OR formatted_ar <> '')
);
CREATE TABLE sna.source_record (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), object_type text NOT NULL, object_id uuid NOT NULL,
 source_type text NOT NULL, source_reference text, captured_at timestamptz, captured_by text,
 accuracy_m numeric, verification_status text NOT NULL DEFAULT 'UNVERIFIED', metadata jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE sna.change_request (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), object_type text NOT NULL, object_id uuid,
 operation text NOT NULL CHECK(operation IN ('CREATE','UPDATE','RETIRE')),
 payload jsonb NOT NULL, reason text NOT NULL, status sna.change_status NOT NULL DEFAULT 'DRAFT',
 requested_by uuid NOT NULL, reviewed_by uuid, approved_by uuid,
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
 CHECK(requested_by IS DISTINCT FROM approved_by)
);
CREATE TABLE sna.audit_event (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, event_time timestamptz NOT NULL DEFAULT now(),
 actor_id uuid, action text NOT NULL, object_type text NOT NULL, object_id uuid,
 before_json jsonb, after_json jsonb, correlation_id uuid, previous_hash text, event_hash text NOT NULL
);

CREATE INDEX admin_unit_geom_gix ON sna.admin_unit USING gist(geom);
CREATE INDEX street_geom_gix ON sna.street USING gist(centreline);
CREATE INDEX parcel_geom_gix ON sna.parcel USING gist(geom);
CREATE INDEX building_geom_gix ON sna.building USING gist(geom);
CREATE INDEX entrance_geom_gix ON sna.entrance USING gist(geom);
CREATE INDEX address_position_gix ON sna.address USING gist(position);
CREATE INDEX address_search_ar_idx ON sna.address USING gin(to_tsvector('simple',formatted_ar));
CREATE INDEX address_search_en_idx ON sna.address USING gin(to_tsvector('simple',coalesce(formatted_en,'')));
CREATE INDEX change_status_idx ON sna.change_request(status,created_at);

REVOKE ALL ON SCHEMA sna FROM PUBLIC;
COMMENT ON SCHEMA sna IS 'Syrian National Address and Geospatial Pilot core registry';
COMMIT;
