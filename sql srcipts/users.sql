use ncat;

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
