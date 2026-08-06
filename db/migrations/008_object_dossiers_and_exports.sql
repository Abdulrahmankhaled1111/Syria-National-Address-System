BEGIN;
CREATE TABLE sna.object_dossier (
 dossier_number text PRIMARY KEY, object_type text NOT NULL,
 object_id uuid NOT NULL, admin_unit_id uuid NOT NULL REFERENCES sna.admin_unit,
 dossier_status text NOT NULL DEFAULT 'OPEN', metadata jsonb NOT NULL DEFAULT '{}',
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(object_type,object_id)
);
CREATE TABLE sna.data_delivery (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), recipient_type text NOT NULL,
 recipient_name text NOT NULL, dataset_type text NOT NULL,
 legal_basis text NOT NULL, license_reference text, filter jsonb NOT NULL DEFAULT '{}',
 record_count integer, checksum text, delivered_at timestamptz,
 approved_by uuid, created_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE sna.data_delivery IS 'Auditable exports to postal, emergency, mapping or other authorized recipients.';
COMMIT;
