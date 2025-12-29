createdb -U postgres async_db
psql -U postgres -d async_db -c "
DROP TABLE IF EXISTS characters;
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    birth_year TEXT,
    eye_color TEXT,
    gender TEXT,
    hair_color TEXT,
    homeworld TEXT,
    mass TEXT,
    name TEXT,
    skin_color TEXT
);
"