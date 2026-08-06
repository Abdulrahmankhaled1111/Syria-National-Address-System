BEGIN;
CREATE TYPE sna.house_number_status AS ENUM ('SUBMITTED','REVIEWED','APPROVED','REJECTED','PUBLISHED');
CREATE TABLE sna.house_number_case (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), building_id uuid NOT NULL REFERENCES sna.building,
 entrance_id uuid REFERENCES sna.entrance, street_id uuid REFERENCES sna.street,
 locality_id uuid NOT NULL REFERENCES sna.admin_unit, proposed_house_number text NOT NULL,
 proposed_postal_code varchar(6) NOT NULL REFERENCES sna.postal_area(postal_code),
 status sna.house_number_status NOT NULL DEFAULT 'SUBMITTED',
 requested_by uuid NOT NULL, reviewed_by uuid, approved_by uuid,
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
 CHECK(requested_by IS DISTINCT FROM approved_by)
);
CREATE UNIQUE INDEX one_active_house_number_case_per_building
 ON sna.house_number_case(building_id) WHERE status IN ('SUBMITTED','REVIEWED','APPROVED');
COMMIT;
