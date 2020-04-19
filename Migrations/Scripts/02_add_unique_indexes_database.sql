CREATE UNIQUE INDEX IF NOT EXISTS login_unique_user ON user (login);

CREATE UNIQUE INDEX IF NOT EXISTS login_unique_user_to_add ON user_to_add (login);