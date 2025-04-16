from src.Database import DataBase
from src.User import User
from src.Constants import *

class App:
    def __init__(self):
        self.db = DataBase()
        self.user = User()
        self.login_attempts = MAX_LOGIN_ATTEMPTS
        
    def run(self):
        self.show_login_menu()
            
        if self.login_attempts == 0:
            print('Login attempts excceded closing program.')
            exit(1)
            
        while True:
            if self.user.roleId == 'stu':
                self.show_student_menu()
            else:
                self.show_manager_menu()

    def show_login_menu(self):
        print(f"NCAT Application Login: \n")
        
        while self.login_attempts > 0:
            print(f'Login attempts remaining {self.login_attempts}\n')
            username = input("Enter User Name: ")
            password = input("Enter User Password: ") 
            
            try:
                self.login(username, password)
                print(f"I am a {self.user.role}")
                break
            except:
                print("Login fails.\n")
                self.login_attempts-=1
                continue
            
    def login(self, username, password):         
        # verifies user in database and returns information relevant for future operations 
        
        # WARNING: the query below is made to work with tables made from create-ncat.sql in the sql scripts folder    
        sql = f"""
                SELECT users.id, fname, lname, role, roleID, majorID FROM users, roles
                WHERE roles.id = users.roleID AND userName = '{username}' AND userPassword = '{password}'
               """
               
        userInfo = self.db.query(sql)   
        print(userInfo)
        self.user.load(userInfo)         

    def show_student_menu(self):
        # will implement later
        pass
    
    def show_manager_menu(self):
        # will implement later
        pass