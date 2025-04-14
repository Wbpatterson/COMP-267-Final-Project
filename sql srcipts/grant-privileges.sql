DROP DATABASE IF EXISTS NCAT;
CREATE DATABASE IF NOT EXISTS NCAT;
USE NCAT;

create user if not exists 'AggieAdmin'@'localhost' identified by 'AggiePride';
grant all privileges on ncat.* to 'AggieAdmin'@'localhost' with grant option;
flush privileges;