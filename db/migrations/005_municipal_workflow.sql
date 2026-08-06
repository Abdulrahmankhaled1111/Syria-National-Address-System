BEGIN;
CREATE TABLE sna.organisation (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organisation_type text NOT NULL,
 name_ar text NOT NULL, name_en text, admin_unit_id uuid REFERENCES sna.admin_unit, active boolean NOT NULL DEFAULT true
);
CREATE TABLE sna.staff_assignment (
 user_id uuid NOT NULL, organisation_id uuid NOT NULL REFERENCES sna.organisation,
 operational_role text NOT NULL CHECK(operational_role IN
 ('MUNICIPAL_EDITOR','SURVEYOR','REVIEWER','APPROVER','PRINT_OFFICER','INSTALLER','AUDITOR','SYSTEM_ADMIN')),
 admin_unit_id uuid REFERENCES sna.admin_unit, valid_from timestamptz NOT NULL DEFAULT now(),
 valid_to timestamptz, PRIMARY KEY(user_id,organisation_id,operational_role)
);
CREATE TABLE sna.field_job (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), address_id uuid NOT NULL REFERENCES sna.address,
 job_type text NOT NULL CHECK(job_type IN ('PLAN_EXPORT','NOTICE_LETTER','PLAQUE_PRODUCTION','PLAQUE_INSTALLATION')),
 status text NOT NULL CHECK(status IN ('CREATED','ASSIGNED','PRINTED','IN_PRODUCTION','READY','INSTALLED','VERIFIED','CANCELLED')),
 assigned_to uuid, created_by uuid NOT NULL, payload jsonb NOT NULL DEFAULT '{}',
 evidence jsonb, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX field_job_status_idx ON sna.field_job(status,job_type);
REVOKE ALL ON sna.field_job FROM PUBLIC;
GRANT SELECT ON sna.field_job TO sna_editor,sna_reviewer,sna_approver,sna_auditor;
COMMIT;
