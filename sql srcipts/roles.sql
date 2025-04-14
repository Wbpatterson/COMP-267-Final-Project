USE ncat;

CREATE TABLE roles(
	id INT PRIMARY KEY AUTO_INCREMENT,
    role VARCHAR(50)
);

INSERT INTO Roles (RoleID, RoleName) VALUES ('mgr', 'Manager');
INSERT INTO Roles (RoleID, RoleName) VALUES ('stu', 'Student');