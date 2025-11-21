CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users_uuid_name (
  id_name UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100)
);

INSERT INTO users_uuid_name (name) VALUES ('Alice');

SELECT * FROM users_uuid_name;