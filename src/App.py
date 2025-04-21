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
        print("\n=== Student Menu ===")
        print("1. View My Classes")
        print("2. Drop a Class")
        print("3. Logout")

        choice = input("Choose an option: ")
    
        if choice == '1':
            self.view_classes()  # Method to view enrolled classes
        elif choice == '2':
            self.drop_class()  # Method to drop a class
        elif choice == '3':
            print("Logging out...\n")
            break  # Exit the menu and go back to login
        else:
            print("Invalid option. Please try again.")

    def view_classes(self):
    # This method should fetch and display the classes the student is enrolled in.
    # assumes `self.user.id` holds the student's ID
    student_id = self.user.id
    query = """
        SELECT c.class_id, c.class_name
        FROM enrollment e
        JOIN class c ON e.class_id = c.class_id
        WHERE e.student_id = %s
    """
    
    # Execute the query to get the classes
    self.db.cursor.execute(query, (student_id,))
    rows = self.db.cursor.fetchall()

    print("\nYour Enrolled Classes:")
    if rows:
        for class_id, class_name in rows:
            print(f"- {class_id}: {class_name}")
    else:
        print("You are not enrolled in any classes.")
    
    def show_manager_menu(self):
        # will implement later
        pass
