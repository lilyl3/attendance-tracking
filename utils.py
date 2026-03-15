from datetime import date, timedelta, datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta

import os as os

def trend_paths(year):
    os.makedirs("trend", exist_ok=True)
    base_dir = Path("trend")
    path = base_dir / f"{str(year)}.csv"
    new_friends_path = base_dir / f"{str(year)} (new).csv"
    return path, new_friends_path

def attendance_file_paths(sunday_date):
    base_dir = Path("sunday_attendance")
    month, year = sunday_date.strftime("%m"), sunday_date.strftime("%Y")
    folder_path = base_dir / year / month
    os.makedirs(folder_path, exist_ok=True)

    sunday_date = format_date(sunday_date, iso=True)
    file_path = folder_path / f"{sunday_date}.csv"
    new_friends_file_path = folder_path / f"{sunday_date} (new).csv"
    return file_path, new_friends_file_path

# Iso formats date as YYYY-MM-DD
def format_date(date_to_format, iso):
    if iso and not isinstance(date_to_format, str):
        return date_to_format.isoformat()
    return date_to_format
    
def today(iso = True):
    return format_date(date.today(), iso)

def most_recent_sunday(iso = True):
    # Return the most recent Sunday
    today = date.today()
    most_recent_sunday = today - timedelta(days=(today.weekday() + 1) % 7) # sunday = 6
    return format_date(most_recent_sunday, iso)

def get_date_months_ago(delta_month = 3, iso = True):
    date_months_ago = most_recent_sunday(iso=False) - relativedelta(months=delta_month)
    return format_date(date_months_ago, iso)