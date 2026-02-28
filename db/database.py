from datetime import date
import sqlite3

from . import schema, sql
import utils

class AttendanceDB():
    def __init__(self, DB_FILENAME):
        self.DB_FILENAME = DB_FILENAME
        # Set up connection to database
        self.conn = sqlite3.connect(self.DB_FILENAME, check_same_thread=False)  # OK if access conn from a different thread
        self.conn.execute("PRAGMA foreign_keys = ON")                           # Enforce foreign keys
        self.create_tables()

    def create_cursor(self):
        return self.conn.cursor()

    # Create table if it does not exist
    def create_tables(self):
        curr = self.create_cursor()
        curr.execute(schema.MEMBERS_TABLE)
        curr.execute(schema.ATTENDANCE_TABLE)
        curr.execute(schema.FAMILY_TABLE)

    def get_member_id(self, name):
        if name is None or name == "":
            return None
        curr = self.create_cursor()
        curr.execute(sql.GET_MEMBER_ID, (name, name))
        row = curr.fetchone()
        member_id = row[0] if row else None
        return member_id

    # Add new member
    def add_member(self, data):
        curr = self.create_cursor()
        for i in range(len(data)):
            if data[i] == "":
                data[i] = None
        curr.execute(sql.ADD_MEMBER, data)
        member_id = curr.lastrowid
        curr.connection.commit()
        return member_id

    def add_family(self, family_name: str, date = None, invited_by_name = None):
        invited_by = self.get_member_id(invited_by_name)
        if date:
            date = utils.format_date(date, iso=True)
        curr = self.create_cursor()
        curr.execute(sql.ADD_FAMILY, (family_name, date, invited_by))
        family_id = curr.lastrowid
        curr.connection.commit()
        return family_id

    # Return all members who attended on most recent dunday
    def get_members(self):
        curr = self.create_cursor()
        most_recent_sunday = utils.most_recent_sunday()
        curr.execute(sql.GET_MEMBERS, (most_recent_sunday, ))
        return curr.fetchall()

    # Mark member's attendance
    def add_attendance(self, member_id):
        curr = self.create_cursor()
        curr.execute(sql.ADD_ATTENDANCE, (member_id, utils.most_recent_sunday()))
        curr.connection.commit()

    def delete_attendance(self, member_id):
        curr = self.create_cursor()
        curr.execute(sql.DELETE_ATTENDANCE, (member_id, utils.most_recent_sunday()))
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
    def get_attendees_on_date(self, date = utils.most_recent_sunday()):
        if not isinstance(date, str):
            date = utils.format_date(date, iso=True)
        curr = self.create_cursor()
        curr.execute(sql.GET_ATTENDEE_NAMES, (date, ))
        return curr.fetchall()
    
    # Query attendance between [start_date, end_date]
    # If start_date is not provided, then return attendance in past 3 months
    def get_attendees_in_date_range(self, start_date = utils.get_date_months_ago(), end_date = utils.today()):
        start_date = utils.format_date(start_date, iso=True)
        end_date = utils.format_date(end_date, iso=True)
        curr = self.create_cursor()
        curr.execute(sql.GET_ATTENDEES_IN_RANGE, (start_date, end_date))
        return curr.fetchall()