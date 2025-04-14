use ncat;
SELECT RoleName FROM Roles, Users
WHERE Roles.RoleID = Users.roleID AND UserName='Student1' AND UserPassword='AggiePride1'