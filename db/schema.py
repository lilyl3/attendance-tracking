# Table Schemas
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
        date TEXT,
        FOREIGN KEY(member_id) REFERENCES members(id)
)"""