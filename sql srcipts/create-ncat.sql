DROP DATABASE IF EXISTS NCAT;
CREATE DATABASE IF NOT EXISTS NCAT;
USE NCAT;

create user if not exists'AggieAdmin'@'localhost' identified by 'AggiePride';
grant all privileges on ncat.* to 'AggieAdmin'@'localhost' with grant option;
flush privileges;

CREATE TABLE major(
	id INT PRIMARY KEY AUTO_INCREMENT,
    major VARCHAR(50)
);

CREATE TABLE roles(
	id   	VARCHAR(50) PRIMARY KEY,
    role 	VARCHAR(50)
);

INSERT INTO Roles (id, role) VALUES ('mgr', 'Manager');
INSERT INTO Roles (id, role) VALUES ('stu', 'Student');

CREATE TABLE users(
id INT(1) PRIMARY KEY AUTO_INCREMENT,
userName VARCHAR(50),
userPassword VARCHAR(50),
roleID VARCHAR(50),
fname varchar(50),
lname varchar(50),
majorID int,
FOREIGN KEY (roleID) REFERENCES roles(id),
FOREIGN KEY (majorID) REFERENCES major(id)
);

INSERT INTO Users (roleID, UserName, UserPassword) VALUES ('mgr', 'Manager1', 'AggiePride1');
INSERT INTO Users (roleID, UserName, UserPassword) VALUES ('stu', 'Student1', 'AggiePride1');

CREATE TABLE roster(
 id   	INT PRIMARY KEY AUTO_INCREMENT,
 class 	VARCHAR(50),
 code 	VARCHAR(20)
);

CREATE TABLE rosterclass(
	rosterid int,
    userid int,
    FOREIGN KEY (rosterid) REFERENCES roster (id),
    FOREIGN KEY (userid) REFERENCES users (id)
);


