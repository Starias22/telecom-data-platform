CREATE TABLE data_quality.issues(
        issue_id SERIAL PRIMARY KEY, -- Big int generated always as identity primary key?
        batch_id VARCHAR(25) NOT NULL,
        table_name VARCHAR(50) NOT NULL,
        column_name VARCHAR(50),
        record_id INT NOT NULL,
        issue_type VARCHAR(25) NOT NULL CHECK (issue_type IN('Completness', 'Uniqueness', 'Validity', 'Consistency', 'Referential Integrity')),
        issue_code VARCHAR(50) NOT NULL,
        issue_description TEXT NOT NULL
       
        -- reject_record BOOLEAN DEFAULT TRUE -- Really important?
        -- detected_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP -- what is TZ? why?
        -- is_fixed?
);