CREATE TABLE IF NOT EXISTS ref.cities(
        id SERIAL PRIMARY KEY,
        city VARCHAR(20) NOT NULL,
        department VARCHAR(20) NOT NULL
);