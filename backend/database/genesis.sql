CREATE TABLE disease_classifications(
    id INTEGER PRIMARY KEY,
    disease_name VARCHAR(32) UNIQUE NOT NULL
);

CREATE TABLE image_logs(
    id INTEGER PRIMARY KEY,
    image_name VARCHAR(128) NOT NULL,
    extension VARCHAR(4) NOT NULL,
    image_path VARCHAR(256) NOT NULL UNIQUE,
    classification VARCHAR(32) NOT NULL,
    processed_at TIMESTAMP NOT NULL DEFAULT datetime,
    FOREIGN KEY (classification) REFERENCES disease_classifications(disease_name)
);

CREATE INDEX image_class ON image_logs(classification);