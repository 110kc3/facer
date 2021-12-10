DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS images;
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  user_id integer primary key autoincrement,
  email string not null,
  sub string not null
);

CREATE TABLE images (
  image_id integer primary key autoincrement,
  name string not null,
  image_location string not null,
  owner_id integer not null,
  FOREIGN key (owner_id) REFERENCES users (user_id)
  
);
