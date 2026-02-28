# Table Schemas
FAMILY_TABLE = """
    CREATE TABLE IF NOT EXISTS family (
        id INTEGER PRIMARY KEY,
        family_name TEXT,
        first_visit_date TEXT,
        invited_by_id INTEGER,
        FOREIGN KEY (invited_by_id) REFERENCES members(id)
)"""

MEMBERS_TABLE = """
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY,
        english_name TEXT,
        chinese_name TEXT,
        gender TEXT,
        age TEXT,
        phone_number TEXT,
        address TEXT,
        language TEXT,
        visit_purpose TEXT,
        initial_faith TEXT,
        family_id INTEGER,
        FOREIGN KEY (family_id) REFERENCES family(id)
)"""

ATTENDANCE_TABLE = """
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        date TEXT,
        FOREIGN KEY(member_id) REFERENCES members(id),
        UNIQUE(member_id, date)
)"""