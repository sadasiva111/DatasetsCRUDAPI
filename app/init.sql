-- init.sql
DO
    $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'obsrv_user') THEN
            CREATE USER obsrv_user WITH PASSWORD 'obsrv123';
        END IF;
    END
    $$;
    
GRANT ALL PRIVILEGES ON DATABASE postgres TO obsrv_user;

CREATE TABLE IF NOT EXISTS datasets (
    id TEXT PRIMARY KEY,
    dataset_id TEXT,
    type TEXT NOT NULL,
    name TEXT,
    validation_config JSON,
    extraction_config JSON,
    dedup_config JSON,
    data_schema JSON,
    denorm_config JSON,
    router_config JSON,
    dataset_config JSON,
    status TEXT,
    tags TEXT[],
    data_version INT,
    created_by TEXT,
    updated_by TEXT,
    created_date TIMESTAMP NOT NULL DEFAULT now(),
    updated_date TIMESTAMP NOT NULL,
    published_date TIMESTAMP NOT NULL DEFAULT now()
);

ALTER TABLE datasets OWNER TO obsrv_user;

ALTER TABLE datasets
ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;
