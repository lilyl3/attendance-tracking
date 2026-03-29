# SQL Statements
ADD_MEMBER = """
    INSERT INTO members 
    (english_name, chinese_name, gender, age, phone_number, address, language, visit_purpose, initial_faith, family_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

UPDATE_MEMBER_INFO = """
    UPDATE members
    SET english_name = ?,
        chinese_name = ?,
        gender = ?, 
        age = ?, 
        phone_number = ?, 
        address = ?, 
        language = ?, 
        initial_faith = ?
    WHERE members.id = ?
"""

GET_MEMBER_FAMILY_INFO = """
    SELECT id, family_id
    FROM members
    WHERE english_name LIKE ?
    OR chinese_name = ?
"""

GET_MEMBER_INFO = """
    SELECT *
    FROM members
    WHERE members.id = ?
"""

GET_MEMBERS_WITH_FAMILY_INITIAL = """
    SELECT members.id || ". " || english_name || ' ' || chinese_name as name
    FROM members
    JOIN family 
    ON family.id = members.family_id
    WHERE family_name LIKE ?
"""

DELETE_MEMBER = """
    DELETE FROM members
    WHERE id = ?
"""

GET_MEMBER_ID = """
    SELECT id
    FROM members
    WHERE english_name = ?
    OR chinese_name = ?
"""

UPDATE_FAMILY_ID = """
    UPDATE members
    SET family_id = ?
    WHERE id = ?
"""

ADD_FAMILY = """
    INSERT INTO family
    (family_name, first_visit_date, invited_by_id)
    VALUES (?, ?, ?)
"""

CLEAN_FAMILY = """
    DELETE FROM family
    WHERE id IN (
        SELECT f.id
        FROM family f
        LEFT JOIN members m
        ON f.id = m.family_id
        WHERE m.id IS NULL
    )
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

GET_NEW_FRIENDS = """
    SELECT m.english_name, m.chinese_name
    FROM members m
    JOIN family f
    ON m.family_id = f.id
    WHERE f.first_visit_date = ?
"""

GET_NEW_FRIENDS_IN_RANGE = """
    SELECT f.first_visit_date
    FROM members m
    JOIN family f
    ON m.family_id = f.id
    WHERE f.first_visit_date LIKE ?
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
    WHERE a.date LIKE ?
"""