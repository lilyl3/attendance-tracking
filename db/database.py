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
    
    def delete_member(self, id):
        curr = self.create_cursor()
        curr.execute(sql.DELETE_MEMBER, (id, ))
        curr.connection.commit()

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
    
    def get_member_info(self, member_id):
        curr = self.create_cursor()
        curr.execute(sql.GET_MEMBER_INFO, (member_id,))
        row = curr.fetchone()
        return row
    
    def update_member_info(self, member_info):
        curr = self.create_cursor()
        curr.execute(sql.UPDATE_MEMBER_INFO, member_info)
        curr.connection.commit()
    
    # Returns (member_id, family_id)
    def get_member_family_info(self, last_name, first_name, chinese_name):
        curr = self.create_cursor()
        curr.execute(sql.GET_MEMBER_FAMILY_INFO, (f"{last_name}, {first_name}", chinese_name))
        row = curr.fetchone()
        return row if row else None
    
    def update_family_id(self, member_id, family_id):
        curr = self.create_cursor()
        curr.execute(sql.UPDATE_FAMILY_ID, (family_id, member_id))
        curr.connection.commit()

    def add_family(self, family_name: str, date, invited_by_name = None):
        invited_by = self.get_member_id(invited_by_name)
        date = utils.format_date(date, iso=True)

        curr = self.create_cursor()
        curr.execute(sql.ADD_FAMILY, (family_name, date, invited_by))
        family_id = curr.lastrowid
        curr.connection.commit()
        return family_id
    
    # Remove all families with no members
    def clean_family(self):
        curr = self.create_cursor()
        curr.execute(sql.CLEAN_FAMILY)
        curr.connection.commit()

    # Return all members who attended on sunday_date
    def get_members(self, sunday_date):
        curr = self.create_cursor()
        sunday_date = utils.format_date(sunday_date, iso=True)
        curr.execute(sql.GET_MEMBERS, (sunday_date, ))
        return curr.fetchall()
    
    def get_members_with_family_initial(self, family_initial):
        curr = self.create_cursor()
        curr.execute(sql.GET_MEMBERS_WITH_FAMILY_INITIAL, (f"{family_initial}%", ))
        return curr.fetchall()

    # Mark member's attendance
    def add_attendance(self, member_id, sunday_date):
        curr = self.create_cursor()
        if not isinstance(date, str):
            sunday_date = utils.format_date(sunday_date, iso=True)
        curr.execute(sql.ADD_ATTENDANCE, (member_id, sunday_date))
        curr.connection.commit()

    def delete_attendance(self, member_id, sunday_date):
        curr = self.create_cursor()
        if not isinstance(date, str):
            sunday_date = utils.format_date(sunday_date, iso=True)
        curr.execute(sql.DELETE_ATTENDANCE, (member_id, sunday_date))
        curr.connection.commit()

    def get_new_friends(self, sunday_date = None):
        curr = self.create_cursor()
        if sunday_date is None:
            sunday_date = utils.most_recent_sunday()
        if not isinstance(date, str):
            sunday_date = utils.format_date(sunday_date, iso=True)
        curr.execute(sql.GET_NEW_FRIENDS, (sunday_date,))
        return curr.fetchall()
    
    def get_new_friends_in_range(self, year):
        curr = self.create_cursor()
        curr.execute(sql.GET_NEW_FRIENDS_IN_RANGE, (str(year) + "%",))
        return curr.fetchall()

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
    
    # Query attendance count in the year provided
    def get_attendees_in_range(self, year):
        curr = self.create_cursor()
        curr.execute(sql.GET_ATTENDEES_IN_RANGE, (str(year) + "%", ))
        return curr.fetchall()