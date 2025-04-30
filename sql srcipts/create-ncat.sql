DROP DATABASE IF EXISTS NCAT;
CREATE DATABASE IF NOT EXISTS NCAT;
USE NCAT;


create user if not exists'AggieAdmin'@'localhost' identified by 'AggiePride';
grant all privileges on ncat.* to 'AggieAdmin'@'localhost' with grant option;
flush privileges;

CREATE TABLE major(
	id      INT PRIMARY KEY AUTO_INCREMENT,
    major   VARCHAR(50)
);

CREATE TABLE roles(
	id   	VARCHAR(50) PRIMARY KEY,
    role 	VARCHAR(50)
);

INSERT INTO Roles (id, role) VALUES ('mgr', 'Manager');
INSERT INTO Roles (id, role) VALUES ('stu', 'Student');

CREATE TABLE users(
    id                  INT(1) PRIMARY KEY AUTO_INCREMENT,
    userName            VARCHAR(50),
    userPassword        VARCHAR(50),
    roleID              VARCHAR(50),
    fname               VARCHAR(50),
    lname               VARCHAR(50),
    majorID             INT,
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
	rosterid    INT,
    userid      INT,
    FOREIGN KEY (rosterid) REFERENCES roster (id),
    FOREIGN KEY (userid) REFERENCES users (id)
);

-- --Below are the sample queries used for the presentation
-- --If you want to go back to the previous layout, delete all the queries below this comment.
-- -- Majors
INSERT INTO major (major) VALUES
('Computer Science'),
('Mathematics'),
('Physics'),
('Biology');

-- Students
INSERT INTO users (fname, lname, userName, userPassword, roleID, majorID) VALUES
('John', 'Doe', 'jdoe', 'password123', 'stu', 1),
('Jane', 'Smith', 'jsmith', 'password456', 'stu', 2),
('Alice', 'Johnson', 'ajohnson', 'password789', 'stu', 3);

-- Manager
INSERT INTO users (fname, lname, userName, userPassword, roleID, majorID) VALUES
('Mary', 'Davis', 'mdavis', 'admin123', 'mgr', 1);

-- Classes
INSERT INTO roster (class, code) VALUES
('Computer Science 101', 'CS101'),
('Mathematics 201', 'MATH201'),
('Physics 301', 'PHYS301'),
('Chemistry 101', 'CHEM101'),
('Biology 202', 'BIO202');

-- Enrollments
INSERT INTO rosterclass (rosterid, userid) VALUES
(1, 3), -- John (id=3) in CS101
(2, 3), -- John (id=3) in MATH201
(3, 4), -- Jane (id=4) in PHYS301
(4, 4), -- Jane (id=4) in CHEM101
(5, 5); -- Alice (id=5) in BIO202


