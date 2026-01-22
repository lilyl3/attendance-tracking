from datetime import date
import sqlite3

import utils, schema, sql

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
        self.cur.execute(schema.MEMBERS_TABLE)
        self.cur.execute(schema.ATTENDANCE_TABLE)

    # Check if person is a member
    def is_member(self, english_name, chinese_name):
        self.cur.execute(sql.IS_MEMBER, (english_name, chinese_name))
        row = self.cur.fetchone()
        if row:
            return True
        return False

    # Add new member
    def add_member(self, english_name, chinese_name):
        if not self.is_member():
            self.cur.execute(sql.ADD_MEMBER, (english_name, chinese_name))

    # Mark member's attendance
    def add_attendance(self, member_id):
        self.cur.execute(sql.ADD_ATTENDANCE, (member_id, utils.today()))

    # Query total attendees on a given day
    # If no date is provided, return the most recent Sunday
    # Returns a number
    def count_attendees(self, date = None):
        if (date is None):
            date = utils.most_recent_sunday()

        self.cur.execute(sql.COUNT_ATTENDEES, (date))
        row = self.cur.fetchone()
        total = row[0] if row else 0
        return total
    
    # Query names of attendees on a given day
    # If no date is provided, return the most recent Sunday
    # Returns a list of tuples
    def get_attendees_on_date(self, date = None):
        if (date is None):
            date = utils.most_recent_sunday()
        self.cur.execute(sql.GET_ATTENDEE_NAMES, (date))
        return self.cur.fetchall()
    
    # Query attendance between [start_date, end_date]
    # If start_date is not provided, then return attendance in past 3 months
    def get_attendees_in_date_range(self, start_date = None, end_date = None):
        if (start_date is None):
            start_date = utils.get_date_months_ago()
        if (end_date is None):
            end_date = utils.today()
        self.cur.execute(sql.GET_ATTENDEES_IN_RANGE, (start_date, end_date))
        return self.cur.fetchall()