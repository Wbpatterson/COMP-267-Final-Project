import mysql.connector
from mysql.connector import errorcode

class DataBase:  
    def __init__(self, uname="AggieAdmin", pname="AggiePride", host="localhost", database="NCAT"):
        self.uname = uname
        self.pname = pname
        self.host = host
        self.database = database
        
        self.connection = None
        self.cursor = None
        self.create_connection()
    
    # closes connection to database automatically after DataBase instance goes out of scope
    def __del__(self):
        self.close()
    
    def create_connection(self):
        if self.is_connected(): self.connection.close()
        
        try:
            self.connection = mysql.connector.connect(
                host= self.host,
                user= self.uname,
                password= self.pname,
                database= self.database
            )
            
            self.cursor = self.connection.cursor()
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid credintials")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database not found")
            else:
                print("Cannot connect to database")
        else:
            print("Connection Successful!!")
            print()
    
    def close(self):
        if not self.connection:
            print("No database connection established.")
        else:
            self.cursor.close()
            self.connection.close()
    
    def is_connected(self):
        if not self.connection:
            return False
        else:
            return True
    
    # returns first row matched from database query 
    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()