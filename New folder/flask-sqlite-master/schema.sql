DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id integer primary key autoincrement,
  name string not null,
  email string not null
);

-- CREATE TABLE images (
--   id integer primary key autoincrement,
--   ownerId integer FOREIGN key REFERENCES users(id),
--   name string not null
-- );
