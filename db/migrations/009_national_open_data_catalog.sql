-- Production/PostGIS counterpart of the compact local national SQLite index.
BEGIN;
CREATE TABLE sna.open_road_object (
 source_id bigint PRIMARY KEY, technical_code text UNIQUE NOT NULL,
 name_ar text,name_en text,name_source text,highway text,ref text,
 representative_position geometry(Point,4326),geom geometry(LineString,4326),
 quality_level sna.quality_level NOT NULL DEFAULT 'D',official_status text NOT NULL DEFAULT 'OPEN_DATA_UNVERIFIED'
);
CREATE TABLE sna.open_building_object (
 source_id bigint PRIMARY KEY,technical_code text UNIQUE NOT NULL,building_type text,
 representative_position geometry(Point,4326),geom geometry(Polygon,4326),
 quality_level sna.quality_level NOT NULL DEFAULT 'D',official_status text NOT NULL DEFAULT 'OPEN_DATA_UNVERIFIED'
);
CREATE INDEX open_road_geom_gix ON sna.open_road_object USING gist(geom);
CREATE INDEX open_building_geom_gix ON sna.open_building_object USING gist(geom);
COMMENT ON TABLE sna.open_building_object IS 'Nationwide open-data working objects. Not authoritative buildings until municipal verification.';
COMMIT;
