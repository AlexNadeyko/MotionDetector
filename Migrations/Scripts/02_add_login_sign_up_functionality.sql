CREATE TABLE IF NOT EXISTS user_to_add (
    login               TEXT        NOT NULL,
    hashed_password     TEXT        NOT NULL,
    date_time           TEXT        NOT NULL
);


CREATE UNIQUE INDEX IF NOT EXISTS login_unique_user ON user (login);
CREATE UNIQUE INDEX IF NOT EXISTS login_unique_user_to_add ON user_to_add (login);

INSERT OR IGNORE  INTO user (login, hashed_password)
VALUES ('admin', 'pbkdf2:sha256:150000$k6deRBT7$2ffd58fcd33e60c5c903fbf2a3a7eb20df15ddbc56bea9214725e55027e39d85');