
CREATE TABLE IF NOT EXISTS user (
    login               TEXT    NOT NULL,
    hashed_password     TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS log (
    date_time       TEXT        NOT NULL,
    is_known        INTEGER     NOT NULL,
    face_image      BLOB        NULL
);

CREATE TABLE IF NOT EXISTS user_to_add (
    login               TEXT        NOT NULL,
    hashed_password     TEXT        NOT NULL,
    date_time           TEXT        NOT NULL
)