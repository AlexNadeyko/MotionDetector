
CREATE TABLE IF NOT EXISTS user (
    login               TEXT    NOT NULL,
    hashed_password     TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS log (
    id_record       INTEGER     PRIMARY KEY     AUTOINCREMENT,
    date            TEXT        NOT NULL,
    time            TEXT        NOT NULL,
    person          TEXT        NOT NULL,
    face_image      BLOB        NOT NULL
)
