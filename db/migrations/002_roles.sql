BEGIN;
DO $$ BEGIN
 CREATE ROLE sna_public NOLOGIN;
 CREATE ROLE sna_editor NOLOGIN;
 CREATE ROLE sna_reviewer NOLOGIN;
 CREATE ROLE sna_approver NOLOGIN;
 CREATE ROLE sna_auditor NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
GRANT USAGE ON SCHEMA sna TO sna_public,sna_editor,sna_reviewer,sna_approver,sna_auditor;
GRANT SELECT ON sna.address,sna.street,sna.admin_unit,sna.entrance,sna.building TO sna_public;
GRANT SELECT ON ALL TABLES IN SCHEMA sna TO sna_editor,sna_reviewer,sna_approver,sna_auditor;
GRANT INSERT ON sna.change_request TO sna_editor;
GRANT UPDATE(status,reviewed_by,updated_at) ON sna.change_request TO sna_reviewer;
GRANT UPDATE(status,approved_by,updated_at) ON sna.change_request TO sna_approver;
GRANT SELECT ON sna.audit_event TO sna_auditor;
REVOKE INSERT,UPDATE,DELETE ON sna.address,sna.street,sna.parcel,sna.building FROM sna_editor,sna_reviewer,sna_approver;
COMMIT;
