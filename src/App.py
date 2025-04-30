from .database import DataBase
from .user import User

MAX_LOGIN_ATTEMPTS = 3

class App:
    def __init__(self):
        self.db = DataBase()
        self.user = User()
        
    def run(self):
        while True:
            self.show_login_menu()

            if self.login_attempts == 0:
                print('Login attempts exceeded. Closing program.')
                exit(1)

            if self.user.roleId == 'stu':
                self.show_student_menu()
            else:
                self.show_manager_menu()
            
    def show_login_menu(self):
        print(f"===:. NCAT Application Login .:=== \n")
        login_attempts = MAX_LOGIN_ATTEMPTS
        
        while login_attempts > 0:
            username = input("Enter User Name: ")
            password = input("Enter User Password: ")


            try:
                self.login(username, password)
                print(f"I am a {self.user.role}")
                break
            except:
                print("Login failed.\n")
                login_attempts -= 1
                print(f'Login attempts remaining {login_attempts}\n')
                continue

    def login(self, username, password):
        # verifies user in database and returns information relevant for future operations

        # WARNING: the query below is made to work with tables made from create-ncat.sql in the sql scripts folder
        sql = f"""
                SELECT users.id, fname, lname, role, roleID, majorID FROM users, roles
                WHERE roles.id = users.roleID AND userName = '{username}' AND userPassword = '{password}'
               """

        userInfo = self.db.query(sql)
        self.user.load(userInfo)

        # HAS NOT BEEN TESTED YET

    def show_student_menu(self):
        while True:
            print("\n====:. Student Menu .:====")
            print("1. View My Classes")
            print("2. Drop a Class")
            print("3. Logout")
            print("==========================")

            choice = input("Choose an option: ")

            if choice == '1':
                self.view_classes()
            elif choice == '2':
                self.drop_class()
            elif choice == '3':
                print("Logging out...\n")
                return  # Go back to run() -> show_login_menu()
            else:
                print("Invalid option. Please try again.")

    def view_classes(self):

        student_id = self.user.id
        query = """
            SELECT r.id, r.class
            FROM rosterclass rc
            JOIN roster r ON rc.rosterid = r.id
            WHERE rc.userid = %s
        """

        self.db.cursor.execute(query, (student_id,))
        rows = self.db.cursor.fetchall()

        if rows:
            print("\nYour Enrolled Classes:")
            print(f"{'Class ID':<10} | {'Class Name'}")
            print("-" * 35)
            for class_id, class_name in rows:
                print(f"{str(class_id):<10} | {class_name}")
        else:
            print("You are not enrolled in any classes.")

    def drop_class(self):
        student_id = self.user.id

        # Fetch the student's enrolled classes
        fetch_query = """
            SELECT r.id, r.class
            FROM rosterclass rc
            JOIN roster r ON rc.rosterid = r.id
            WHERE rc.userid = %s
        """
        self.db.cursor.execute(fetch_query, (student_id,))
        enrolled_classes = self.db.cursor.fetchall()

        if not enrolled_classes:
            print("You are not enrolled in any classes.")
            return

        # Show enrolled classes in table format
        print("\nYour Enrolled Classes:")
        print(f"{'Class ID':<10} | {'Class Name'}")
        print("-" * 35)

        class_ids = {}
        for class_id, class_name in enrolled_classes:
            print(f"{str(class_id):<10} | {class_name}")
            class_ids[str(class_id)] = class_name

        print("\nEnter the Class ID(s) you want to drop, separated by commas (or type 'cancel' to go back):")

        while True:
            user_input = input("Class ID(s): ").strip()

            if user_input.lower() == 'cancel':
                print("Canceled dropping classes.")
                return

            selected_ids = [cid.strip() for cid in user_input.split(',') if cid.strip()]
            invalid_ids = [cid for cid in selected_ids if cid not in class_ids]

            if invalid_ids:
                print(f"Invalid Class ID(s): {', '.join(invalid_ids)}. Please try again.")
                continue

            # Confirm class deletion
            print("\nYou are about to drop the following class(es):")
            print(f"{'Class ID':<10} | {'Class Name'}")
            print("-" * 35)
            for cid in selected_ids:
                print(f"{cid:<10} | {class_ids[cid]}")

            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Canceled dropping classes.")
                return

            # Execute class deletion
            delete_query = """
                DELETE FROM rosterclass WHERE userid = %s AND rosterid = %s
            """
            for cid in selected_ids:
                self.db.cursor.execute(delete_query, (student_id, cid))
            self.db.connection.commit()

            print("Selected class(es) successfully dropped.")
            return

    def show_manager_menu(self):
        while True:
            print("\n=========:. Manager Menu .:=========")
            print("1. View a Student's Class Schedule")
            print("2. View a Class Roster")
            print("3. Add a Student to a Roster")
            print("4. Drop a Student from a Roster")
            print("5. Add a New Student")
            print("6. Logout")
            print("====================================")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                self.view_student_schedule()
            elif choice == '2':
                self.view_class_roster()
            elif choice == '3':
                self.add_student_to_roster()
            elif choice == '4':
                self.drop_student_from_roster()
            elif choice == '5':
                self.add_new_student()
            elif choice == '6':
                print("Logging out...\n")
                break

            else:
                print("Invalid option. Please try again.")

    def view_student_schedule(self):
        # Display all students first
        self.db.cursor.execute("SELECT id, fname, lname FROM users WHERE roleID = 'stu'")
        students = self.db.cursor.fetchall()

        if not students:
            print("No students found.")
            return

        print("\nAvailable Students:")
        print(f"{'ID':<5} | {'First Name':<15} | {'Last Name'}")
        print("-" * 40)
        for sid, fname, lname in students:
            print(f"{sid:<5} | {fname or 'N/A':<15} | {lname or 'N/A'}")

        student_id = input("\nEnter the Student's ID to view schedule: ").strip()
        if not student_id.isdigit():
            print("Invalid ID format. Must be a number.")
            return

        self.db.cursor.execute("SELECT fname, lname FROM users WHERE id = %s", (student_id,))
        student = self.db.cursor.fetchone()

        if student:
            first_name, last_name = student
            print(f"\nViewing Class Schedule for {first_name or 'N/A'} {last_name or 'N/A'}:")
        else:
            print("Student not found.")
            return

        query_classes = """
            SELECT r.id, r.class, r.code
            FROM rosterclass rc
            JOIN roster r ON rc.rosterid = r.id
            WHERE rc.userid = %s
        """
        self.db.cursor.execute(query_classes, (student_id,))
        rows = self.db.cursor.fetchall()

        print("\nStudent's Class Schedule:")
        if rows:
            print(f"{'Class ID':<10} | {'Class Name':<25} | {'Code'}")
            print("-" * 50)
            for class_id, class_name, code in rows:
                print(f"{str(class_id):<10} | {class_name:<25} | {code}")
        else:
            print("Student is not enrolled in any classes.")

    def view_class_roster(self):
        # Show classes to the user
        self.db.cursor.execute("SELECT class, code FROM roster")
        classes = self.db.cursor.fetchall()

        if not classes:
            print("No classes found.")
            return

        print("\nAvailable Classes:")
        print(f"{'Class Name':<30} | {'Code'}")
        print("-" * 45)
        for cname, code in classes:
            print(f"{cname:<30} | {code}")

        class_code = input("\nEnter the Class Code (e.g., CS101): ").strip().upper()

        # Get the roster ID using class   
        self.db.cursor.execute("SELECT id FROM roster WHERE code = %s", (class_code,))
        result = self.db.cursor.fetchone()

        if not result:
            print("Class code not found.")
            return

        class_id = result[0]

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
            print(f"{'Student ID':<12} | {'First Name':<15} | {'Last Name'}")
            print("-" * 45)
            for sid, fname, lname in rows:
                print(f"{sid:<12} | {(fname or 'N/A'):<15} | {lname or 'N/A'}")
        else:
            print("No students enrolled in this class.")

    def add_student_to_roster(self):
        fname = input("First Name: ").strip()
        lname = input("Last Name: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Show majors in a table-like format
        self.db.cursor.execute("SELECT id, major FROM major")
        majors = self.db.cursor.fetchall()
        print("\nAvailable Majors:")
        print(f"{'Major ID':<10} | {'Major Name'}")
        print("-" * 30)
        for mid, mname in majors:
            print(f"{mid:<10} | {mname}")

        major_id = input("\nEnter the Major ID: ").strip()
        if not all([fname, lname, username, password, major_id]):
            print("All fields are required.")
            return
        if not major_id.isdigit():
            print("Major ID must be numeric.")
            return

        self.db.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if self.db.cursor.fetchone():
            print("Username already exists. Choose another.")
            return

        # Show classes in a table-like format
        self.db.cursor.execute("SELECT code, class FROM roster")
        classes = self.db.cursor.fetchall()
        print("\nAvailable Classes:")
        print(f"{'Class Code':<12} | {'Class Name'}")
        print("-" * 30)
        for code, cname in classes:
            print(f"{code:<12} | {cname}")

        class_code = input("\nEnter the Class Code to enroll (e.g., CS101): ").strip().upper()

        self.db.cursor.execute("SELECT id FROM roster WHERE code = %s", (class_code,))
        result = self.db.cursor.fetchone()
        if not result:
            print("Class code not found.")
            return
        class_id = result[0]

        insert_user = """
            INSERT INTO users (roleID, userName, userPassword, fname, lname, majorID)
            VALUES ('stu', %s, %s, %s, %s, %s)
        """
        self.db.cursor.execute(insert_user, (username, password, fname, lname, major_id))
        self.db.connection.commit()

        student_id = self.db.cursor.lastrowid

        self.db.cursor.execute("INSERT INTO rosterclass (rosterid, userid) VALUES (%s, %s)", (class_id, student_id))
        self.db.connection.commit()

        print("Student added and enrolled in class successfully.")

    def drop_student_from_roster(self):
        # Step 1: Show all students with IDs
        self.db.cursor.execute("SELECT id, fname, lname FROM users WHERE roleID = 'stu' ORDER BY lname, fname")
        students = self.db.cursor.fetchall()

        print("\nStudents:")
        print(f"{'ID':<5} | {'First Name':<15} | {'Last Name':<15}")
        print("-" * 40)
        for sid, fname, lname in students:
            print(f"{sid:<5} | {(fname or 'N/A'):<15} | {(lname or 'N/A'):<15}")

        student_id = input("\nEnter the Student ID to remove from a class: ").strip()
        if not student_id.isdigit():
            print("Invalid Student ID.")
            return

        # Step 2: Show classes the student is enrolled in
        query = """
            SELECT r.id, r.class
            FROM rosterclass rc
            JOIN roster r ON rc.rosterid = r.id
            WHERE rc.userid = %s
        """
        self.db.cursor.execute(query, (student_id,))
        enrolled_classes = self.db.cursor.fetchall()

        if not enrolled_classes:
            print("This student is not enrolled in any classes.")
            return

        print("\nEnrolled Classes:")
        print(f"{'Class ID':<10} | {'Class Name'}")
        print("-" * 40)
        for cid, cname in enrolled_classes:
            print(f"{cid:<10} | {cname}")

        class_id = input("\nEnter the Class ID to drop the student from: ").strip()
        if not class_id.isdigit():
            print("Invalid Class ID.")
            return

        # Step 3: Remove from class
        delete_query = "DELETE FROM rosterclass WHERE userid = %s AND rosterid = %s"
        self.db.cursor.execute(delete_query, (student_id, class_id))
        self.db.connection.commit()
        print("Student successfully removed from the class.")

    # THIS ONE STILL NEEDS WORK
    def add_new_student(self):
        fname = input("First Name: ").strip()
        lname = input("Last Name: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Show available majors
        self.db.cursor.execute("SELECT id, major FROM major")
        majors = self.db.cursor.fetchall()
        print("\nAvailable Majors:")
        for mid, mname in majors:
            print(f"{mid}: {mname}")

        major_id = input("Major ID: ").strip()

        if not all([fname, lname, username, password, major_id]):
            print("All fields are required. Please try again.")
            return

        if not major_id.isdigit():
            print("Major ID must be numeric.")
            return

        # Check if username already exists
        self.db.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if self.db.cursor.fetchone():
            print("Username already exists. Choose another one.")
            return

        insert_query = """
            INSERT INTO users (roleID, userName, userPassword, fname, lname, majorID)
            VALUES ('stu', %s, %s, %s, %s, %s)
        """
        self.db.cursor.execute(insert_query, (username, password, fname, lname, major_id))
        self.db.connection.commit()
        print("Student successfully added.")