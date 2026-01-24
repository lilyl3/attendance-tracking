from datetime import date
import sqlite3

from . import schema, sql
import utils

class AttendanceDB():
    def __init__(self, DB_FILENAME):
        self.DB_FILENAME = DB_FILENAME
        self.create_tables()

    def create_cursor(self):
        conn = sqlite3.connect(self.DB_FILENAME)    # Set up connection to database
        conn.execute("PRAGMA foreign_keys = ON")    # Enforce foreign keys
        return conn.cursor()

    # Create table if it does not exist
    def create_tables(self):
        curr = self.create_cursor()
        curr.execute(schema.MEMBERS_TABLE)
        curr.execute(schema.ATTENDANCE_TABLE)

    # Check if person is a member
    def is_member(self, english_name, chinese_name):
        curr = self.create_cursor()
        curr.execute(sql.IS_MEMBER, (english_name, chinese_name))
        row = curr.fetchone()
        if row:
            return True
        return False

    # Add new member
    def add_member(self, english_name, chinese_name):
        if not self.is_member(english_name, chinese_name):
            print("adding member", english_name)
            curr = self.create_cursor()
            curr.execute(sql.ADD_MEMBER, (english_name, chinese_name))
            curr.connection.commit()

    # Return all members
    def get_members(self):
        curr = self.create_cursor()
        most_recent_sunday = utils.most_recent_sunday()
        curr.execute(sql.GET_MEMBERS, (most_recent_sunday, ))
        return curr.fetchall()

    # Mark member's attendance
    def add_attendance(self, member_id):
        curr = self.create_cursor()
        curr.execute(sql.ADD_ATTENDANCE, (member_id, utils.today()))
        curr.connection.commit()

    # Query total attendees on a given day
    # If no date is provided, return the most recent Sunday
    # Returns a number
    def count_attendees(self, date = None):
        if (date is None):
            date = utils.most_recent_sunday()

        curr = self.create_cursor()
        curr.execute(sql.COUNT_ATTENDEES, (date, ))
        row = curr.fetchone()
        total = row[0] if row else 0
        return total
    
    # Query names of attendees on a given day
    # If no date is provided, return the most recent Sunday
    # Returns a list of tuples
    def get_attendees_on_date(self, date = None):
        if (date is None):
            date = utils.most_recent_sunday()
        curr = self.create_cursor()
        curr.execute(sql.GET_ATTENDEE_NAMES, (date))
        return curr.fetchall()
    
    # Query attendance between [start_date, end_date]
    # If start_date is not provided, then return attendance in past 3 months
    def get_attendees_in_date_range(self, start_date = None, end_date = None):
        if (start_date is None):
            start_date = utils.get_date_months_ago()
        if (end_date is None):
            end_date = utils.today()
        curr = self.create_cursor()
        curr.execute(sql.GET_ATTENDEES_IN_RANGE, (start_date, end_date))
        return curr.fetchall()