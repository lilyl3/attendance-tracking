# SQL Statements
ADD_MEMBER = """
    INSERT into members VALUES (?, ?)
"""

ADD_ATTENDANCE = """
    INSERT INTO attendance VALUES (?, ?)
"""

IS_MEMBER = """
    SELECT id
    FROM members
    WHERE english_name = ?
    AND chinese_name = ?
"""

COUNT_ATTENDEES = """
    SELECT COUNT(*)
    FROM attendance
    WHERE date = ?
"""

GET_ATTENDEE_NAMES = """
    SELECT english_name, chinese_name
    FROM members JOIN attendance
    ON members.id = attendance.member_id
    WHERE date = ?
"""

GET_ATTENDEES_IN_RANGE = """
    SELECT members.id, english_name, chinese_name, year, month, day
    FROM members JOIN attendance
    ON members.id = attendance.member_id
    WHERE date >= ? AND date <= ?
"""