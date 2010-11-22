DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS usr CASCADE;
DROP TABLE IF EXISTS video CASCADE;
DROP TABLE IF EXISTS configs CASCADE;

CREATE TABLE sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

CREATE TABLE usr (
       id serial NOT NULL PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(50) NOT NULL,
       name VARCHAR(50),
       surname VARCHAR(50)
);

CREATE TABLE video(
       id serial NOT NULL PRIMARY KEY,
       name VARCHAR(80) NOT NULL,
       format VARCHAR(20) NOT NULL,
       id_owner integer NOT NULL REFERENCES usr(id)
);

CREATE TABLE configs(
       cfgkey VARCHAR(50) NOT NULL PRIMARY KEY,
       cfgvalue VARCHAR(200) NOT NULL
);
