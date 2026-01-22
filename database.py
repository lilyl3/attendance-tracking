import sqlite3
from datetime import date

MEMBERS_TABLE = """
    CREATE TABLE members (
        id INTEGER PRIMARY KEY,
        english_name TEXT,
        chinese_name TEXT
)"""

ATTENDANCE_TABLE = """
    CREATE TABLE attendance (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        FOREIGN KEY(member_id) REFERENCES members(id)
)"""

class AttendanceDB():
    def __init__(self, DB_FILENAME):
        self.DB_FILENAME = DB_FILENAME

        # Set up connection to database
        self.conn = sqlite3.connect(self.DB_FILENAME)
        # Enforce foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.curr = self.conn.cursor()

        self.create_tables()

    # Create table if it does not exist
    def create_tables(self):
        self.cur.execute(MEMBERS_TABLE)
        self.cur.execute(ATTENDANCE_TABLE)

    # Mark member's attendance
    def add_attendance(self, member_id):
        today = date.today()
        self.cur.execute(f"""INSERT INTO attendance VALUES
            ({member_id}, {today.year}, {today.month}, {today.day})
        """)

    # Add new member
    def add_member(self, english_name, chinese_name):
        self.cur.execute(f"""INSERT INTO members VALUES
            ({english_name}, {chinese_name})
        """)

    

    