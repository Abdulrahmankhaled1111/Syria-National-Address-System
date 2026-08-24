BEGIN;

CREATE TABLE IF NOT EXISTS sna.inter_authority_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL CHECK (length(trim(title)) BETWEEN 1 AND 180),
    case_type text NOT NULL CHECK (case_type IN (
        'BUILDING_PERMIT','BOUNDARY_REVIEW','ADDRESS_ASSIGNMENT',
        'DATA_CORRECTION','INTER_AUTHORITY_REVIEW','COORDINATION')),
    priority text NOT NULL DEFAULT 'NORMAL' CHECK (priority IN ('LOW','NORMAL','HIGH','CRITICAL')),
    status text NOT NULL DEFAULT 'OPEN' CHECK (status IN (
        'OPEN','ACCEPTED','IN_PROGRESS','RETURNED','COMPLETED','CANCELLED')),
    source_admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit(id),
    target_admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit(id),
    assigned_role text NOT NULL,
    due_at timestamptz,
    related_object_type text,
    related_object_id uuid,
    description text NOT NULL DEFAULT '',
    created_by uuid NOT NULL,
    assigned_to uuid,
    resolution text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (source_admin_unit_id <> target_admin_unit_id OR case_type IN ('DATA_CORRECTION','COORDINATION')),
    CHECK (status NOT IN ('COMPLETED','RETURNED') OR length(trim(coalesce(resolution,''))) > 0)
);

CREATE INDEX IF NOT EXISTS inter_authority_case_scope_status_idx
    ON sna.inter_authority_case (source_admin_unit_id,target_admin_unit_id,status,due_at);
CREATE INDEX IF NOT EXISTS inter_authority_case_assignee_idx
    ON sna.inter_authority_case (assigned_to,status) WHERE status NOT IN ('COMPLETED','CANCELLED');

REVOKE ALL ON sna.inter_authority_case FROM PUBLIC;
GRANT SELECT,INSERT,UPDATE ON sna.inter_authority_case TO sna_editor,sna_reviewer,sna_approver;
GRANT SELECT ON sna.inter_authority_case TO sna_auditor;

COMMIT;
