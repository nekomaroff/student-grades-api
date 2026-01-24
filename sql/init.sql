DROP TABLE IF EXISTS grades;

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    grade_date DATE NOT NULL,
    group_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade IN (2, 3, 4, 5))
);