from Database import DataBase

def view_classes(student_id, db):
    query = """
        SELECT c.class_id, c.class_name
        FROM enrollment e
        JOIN class c ON e.class_id = c.class_id
        WHERE e.student_id = %s
    """
    db.cursor.execute(query, (student_id,))
    rows = db.cursor.fetchall()

    print("\nYour Enrolled Classes:")
    if rows:
        for class_id, class_name in rows:
            print(f"- {class_id}: {class_name}")
    else:
        print("You are not enrolled in any classes.")


def drop_class(student_id, db):
    print("\nHere are your enrolled classes:")
    view_classes(student_id, db)

    class_id = input("\nEnter the Class ID you want to drop: ").strip()

    # Check if enrolled
    check = """
        SELECT c.class_name
        FROM enrollment e
        JOIN class c ON e.class_id = c.class_id
        WHERE e.student_id = %s AND e.class_id = %s
    """
    db.cursor.execute(check, (student_id, class_id))
    record = db.cursor.fetchone()

    if record:
        class_name = record[0]
        delete = """
            DELETE FROM enrollment
            WHERE student_id = %s AND class_id = %s
        """
        db.cursor.execute(delete, (student_id, class_id))
        db.connection.commit()
        print(f"\n Successfully dropped '{class_name}' (ID: {class_id}).")
    else:
        print("\n You are not enrolled in this class.")


def student_menu(student_id):
    db = DataBase()  # Assumes DataBase connects and sets .cursor and .connection

    try:
        while True:
            print("\n=== Student Menu ===")
            print("1. View My Classes")
            print("2. Drop a Class")
            print("3. Exit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                view_classes(student_id, db)
            elif choice == '2':
                drop_class(student_id, db)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    finally:
        db.cursor.close()
        db.connection.close()
