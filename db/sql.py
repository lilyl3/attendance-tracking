# SQL Statements
ADD_MEMBER = """
    INSERT INTO members 
    (english_name, chinese_name, gender, age, phone_number, address, language, visit_purpose, initial_faith, family_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

GET_MEMBER_ID = """
    SELECT id
    FROM members
    WHERE english_name = ?
    OR chinese_name = ?
"""

ADD_FAMILY = """
    INSERT INTO family
    (family_name, first_visit_date, invited_by_id)
    VALUES (?, ?, ?)
"""

ADD_ATTENDANCE = """
    INSERT OR IGNORE 
    INTO attendance (member_id, date)
    VALUES (?, ?)
"""

DELETE_ATTENDANCE = """
    DELETE FROM attendance
    WHERE member_id = ?
    AND attendance.date = ?;
"""

COUNT_ATTENDEES = """
    SELECT COUNT(*)
    FROM attendance
    WHERE attendance.date = ?
"""

GET_MEMBERS = """
    SELECT m.id, f.family_name, f.id, m.english_name, m.chinese_name, a.id
    FROM family f
    JOIN members m
    ON f.id = m.family_id
    LEFT JOIN attendance a
    ON m.id = a.member_id
    AND a.date = ?
"""

GET_ATTENDEE_NAMES = """
    SELECT m.english_name, m.chinese_name
    FROM members m
    JOIN attendance a
    ON m.id = a.member_id
    WHERE a.date = ?
"""

# For each date in the range
# return N * date rows, where N is the number of attendees on that date
GET_ATTENDEES_IN_RANGE = """
    SELECT a.date
    FROM members m
    JOIN attendance a
    ON m.id = a.member_id
    WHERE a.date >= ? AND a.date <= ?
"""