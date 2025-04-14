from Database import DataBase

class App:
    def __init__(self):
        self.db = DataBase()
        self.title = self.db.database.upper()
        
    def run(self):
        login_attempts = 0
        
        
        print(f"{self.title} Application Login: ")
        print()
        
        while login_attempts < 3:
            username = input("Enter User Name: ")
            password = input("Enter User Password: ") 
            
            try:
                self.login(username, password)
                break
            except:
                print("Login fails.")
                print()
        
    def login(self, username, password):         
        # verifies user in database and returns their RoleName (Manager, Student)
        sql = f"""
                SELECT RoleName FROM Roles, Users
                WHERE Roles.RoleID = Users.roleID AND UserName='{username}' AND UserPassword='{password}'
               """
        result = self.db.query(sql)   
        
        print(f"I am a {result[0]}")
