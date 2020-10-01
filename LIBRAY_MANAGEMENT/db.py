import sqlite3

def checkSetup():
    conn = sqlite3.connect('library_administration.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin'")
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return True

def setup():
    conn = sqlite3.connect('library_administration.db')
    cursor = conn.cursor()
    create_admin_table = """
        CREATE TABLE IF NOT EXISTS admin (
            "id"	TEXT NOT NULL,
			"name"	TEXT NOT NULL,
			"password"	TEXT NOT NULL,
			"secQuestion"	TEXT NOT NULL,
			"secAnswer"	TEXT NOT NULL,
			"Phone"	INTEGER NOT NULL CHECK(10),
			"City"	TEXT NOT NULL
        );
    """
    create_books_table = """
        CREATE TABLE IF NOT EXISTS books (
            "Book_Id"	INTEGER NOT NULL UNIQUE,
			"Book_name"	TEXT NOT NULL,
			"Author"	TEXT NOT NULL,
			"Availiability"	BOOLEAN NOT NULL,
			PRIMARY KEY("Book_Id") 
        );
    """
    create_issue_table = """
        CREATE TABLE IF NOT EXISTS issue (
            "BID"	INTEGER NOT NULL,
			"SID"	INTEGER NOT NULL,
			"Issue_date"	DATE NOT NULL,
			"Return_date"	DATE NOT NULL,
			PRIMARY KEY("BID","SID"),
			FOREIGN KEY("BID") REFERENCES "books"("Book_Id"),
			FOREIGN KEY("SID") REFERENCES "students"("Student_Id")
        );
    """
    create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
            "Roll_no"	INTEGER NOT NULL UNIQUE,
			"name"	TEXT NOT NULL,
			"Student_Id"	INTEGER NOT NULL UNIQUE,
			"class"	INTEGER NOT NULL,
			"Phone_number"	INTEGER NOT NULL CHECK(10),
			"Image"	BLOB NOT NULL,
			"Books_Issued"	INTEGER NOT NULL DEFAULT 0,
			"Fine"	INTEGER NOT NULL DEFAULT 0,
			PRIMARY KEY("Student_Id","Roll_no")
        );
    """
    # create_studentlogin_table = """
    #     CREATE TABLE IF NOT EXISTS studentlogin (
    #       id INTEGER UNIQUE NOT NULL ,
    #       Std_Id INTEGER NOT NULL ,
    #       password TEXT NOT NULL,
    #       FOREIGN KEY("Std_Id") REFERENCES "students"("Student_Id")
    #       );
    # """
    cursor.execute(create_admin_table)
    cursor.execute(create_books_table)
    cursor.execute(create_issue_table)
    cursor.execute(create_students_table)
    # cursor.execute(create_studentlogin_table)
    conn.commit()
    conn.close()


def getConnection():
    return sqlite3.connect('library_administration.db')
