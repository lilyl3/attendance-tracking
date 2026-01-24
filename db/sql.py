# SQL Statements
ADD_MEMBER = """
    INSERT into members (english_name, chinese_name)
    VALUES (?, ?)
"""

ADD_ATTENDANCE = """
    INSERT INTO attendance (member_id, date)
    VALUES (?, ?)
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

GET_MEMBERS = """
    SELECT members.id, english_name, chinese_name, date
    FROM members
    LEFT JOIN attendance
    ON members.id = attendance.member_id
    AND date = ?
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