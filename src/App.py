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

    # HAS NOT BEEN TESTED YET
    def show_student_menu(self):
        while True:
            print("\n=== Student Menu ===")
            print("1. View My Classes")
            print("2. Drop a Class")
            print("3. Logout")
    
            choice = input("Choose an option: ")
    
            if choice == '1':
                self.view_classes()
            elif choice == '2':
                self.drop_class()
            elif choice == '3':
                print("Logging out...\n")
                break  # Exit loop to log out
            else:
                print("Invalid option. Please try again.")


    # HAS NOT BEEN TESTED YET
    def view_classes(self):
        # Fetch and display the classes the student is enrolled in.
        # Matches tables from create-ncat.sql (roster, rosterclass).
        
        student_id = self.user.id
        query = """
            SELECT r.id, r.class
            FROM rosterclass rc
            JOIN roster r ON rc.rosterid = r.id
            WHERE rc.userid = %s
        """
        
        self.db.cursor.execute(query, (student_id,))
        rows = self.db.cursor.fetchall()
    
        print("\nYour Enrolled Classes:")
        if rows:
            for class_id, class_name in rows:
                print(f"- {class_id}: {class_name}")
        else:
            print("You are not enrolled in any classes.")

    # HAS NOT BEEN TESTED YET
    # To Willie: this method was originally several methods. I tried folding them into one, but i haven't tested it yet. 
    # Same for the student menu method and view_classes method.
    def show_manager_menu(self):
    while True:
        print("\n=== Manager Menu ===")
        print("1. View a Student's Class Schedule")
        print("2. View a Class Roster")
        print("3. Add a Student to a Roster")
        print("4. Drop a Student from a Roster")
        print("5. Add a New Student")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            student_id = input("Enter the student's ID: ").strip()
            query = """
                SELECT r.id, r.class, r.code
                FROM rosterclass rc
                JOIN roster r ON rc.rosterid = r.id
                WHERE rc.userid = %s
            """
            self.db.cursor.execute(query, (student_id,))
            rows = self.db.cursor.fetchall()

            print("\nStudent's Class Schedule:")
            if rows:
                for class_id, class_name, code in rows:
                    print(f"- {class_id}: {class_name} (Code: {code})")
            else:
                print("Student is not enrolled in any classes.")

        elif choice == '2':
            class_id = input("Enter the Class ID: ").strip()
            query = """
                SELECT u.id, u.fname, u.lname
                FROM rosterclass rc
                JOIN users u ON rc.userid = u.id
                WHERE rc.rosterid = %s
            """
            self.db.cursor.execute(query, (class_id,))
            rows = self.db.cursor.fetchall()

            print("\nClass Roster:")
            if rows:
                for sid, fname, lname in rows:
                    print(f"- {sid}: {fname} {lname}")
            else:
                print("No students enrolled in this class.")

        elif choice == '3':
            student_id = input("Enter the Student ID: ").strip()
            class_id = input("Enter the Class ID: ").strip()

            check_query = """
                SELECT * FROM rosterclass WHERE userid = %s AND rosterid = %s
            """
            self.db.cursor.execute(check_query, (student_id, class_id))
            if self.db.cursor.fetchone():
                print("Student is already enrolled in this class.")
                continue

            insert_query = """
                INSERT INTO rosterclass (rosterid, userid) VALUES (%s, %s)
            """
            self.db.cursor.execute(insert_query, (class_id, student_id))
            self.db.connection.commit()
            print("Student successfully added to the class.")

        elif choice == '4':
            student_id = input("Enter the Student ID: ").strip()
            class_id = input("Enter the Class ID: ").strip()

            delete_query = """
                DELETE FROM rosterclass WHERE userid = %s AND rosterid = %s
            """
            self.db.cursor.execute(delete_query, (student_id, class_id))
            self.db.connection.commit()
            print("Student successfully removed from the class.")

        elif choice == '5':
            fname = input("First Name: ").strip()
            lname = input("Last Name: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            major_id = input("Major ID: ").strip()

            insert_query = """
                INSERT INTO users (roleID, userName, userPassword, fname, lname, majorID)
                VALUES ('stu', %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(insert_query, (username, password, fname, lname, major_id))
            self.db.connection.commit()
            print("Student successfully added.")

        elif choice == '6':
            print("Logging out...\n")
            break

        else:
            print("Invalid option. Please try again.")

