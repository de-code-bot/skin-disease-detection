CREATE TABLE disease_classifications(
    id INTEGER PRIMARY KEY,
    disease_name VARCHAR(32) UNIQUE NOT NULL
);

CREATE TABLE image_logs(
    id INTEGER PRIMARY KEY,
    image_name VARCHAR(128) NOT NULL,
    extension VARCHAR(4) NOT NULL,   
    classification VARCHAR(32) NOT NULL,
    FOREIGN KEY (classification) REFERENCES disease_classifications(disease_name)
);

CREATE INDEX image_class ON image_logs(classification);