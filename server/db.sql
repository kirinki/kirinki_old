DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS video CASCADE;
DROP TABLE IF EXISTS usr CASCADE;
DROP TABLE IF EXISTS usrType CASCADE;
DROP TABLE IF EXISTS configs CASCADE;

CREATE TABLE sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

CREATE TABLE usrType (
       idType serial NOT NULL PRIMARY KEY,
       tName VARCHAR(50) NOT NULL UNIQUE,
       tDescription VARCHAR(200)
);

CREATE TABLE usr (
       idUsr serial NOT NULL PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(50) NOT NULL,
       name VARCHAR(50),
       surname VARCHAR(50),
       email VARCHAR(50),
       usrType integer NOT NULL REFERENCES usrType(idType)
);

CREATE TABLE video(
       idVideo serial NOT NULL PRIMARY KEY,
       name VARCHAR(80) NOT NULL,
       format VARCHAR(20) NOT NULL,
       id_owner integer NOT NULL REFERENCES usr(idUsr)
);

CREATE TABLE configs(
       cfgkey VARCHAR(50) NOT NULL PRIMARY KEY,
       cfgvalue VARCHAR(200) NOT NULL
);
