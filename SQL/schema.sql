-- PulseMap India — SQLite Schema
-- Created by: Asheer Ahmad
-- Data Source: NFHS-5 (data.gov.in)

CREATE TABLE IF NOT EXISTS districts (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    district              TEXT NOT NULL,
    state                 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS health_metrics (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id           INTEGER REFERENCES districts(id),
    bmi_below_normal_w    REAL,
    overweight_obese_w    REAL,
    anaemia_w             REAL,
    blood_sugar_w         REAL,
    blood_sugar_m         REAL,
    bp_elevated_w         REAL,
    bp_elevated_m         REAL,
    tobacco_w             REAL,
    tobacco_m             REAL,
    alcohol_w             REAL,
    alcohol_m             REAL,
    cervical_screening_w  REAL,
    breast_exam_w         REAL,
    oral_exam_w           REAL
);

CREATE TABLE IF NOT EXISTS socioeconomic (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id       INTEGER REFERENCES districts(id),
    literacy_w        REAL,
    health_insurance  REAL,
    clean_water       REAL,
    sanitation        REAL,
    clean_fuel        REAL
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id INTEGER REFERENCES districts(id),
    risk_score  REAL,
    risk_tier   TEXT,
    cluster     INTEGER
);