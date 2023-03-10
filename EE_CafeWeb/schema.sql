DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS networks;
DROP TABLE IF EXISTS devices;

/*
    Here we make a simple layout for the data we need.
*/

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    permissions TEXT UNIQUE NOT NULL,
    teamname TEXT NOT NULL,
    password TEXT NOT NULL,
);

CREATE TABLE networks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    network_id TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (teamname) REFERENCES user (id)
);

CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    network_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    FOREIGN KEY (teamname) REFERENCES user (id)
);

CREATE TABLE bandwidthPerc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    network_id TEXT NOT NULL,
    bandwidthpercentage INTEGER NOT NULL,
    FOREIGN KEY (teamname) REFERENCES user (id)
)

CREATE TABLE totaldata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    network_id TEXT NOT NULL,
    dataconsumed FLOAT NOT NULL,
    FOREIGN KEY (teamname) REFERENCES user (id)
)