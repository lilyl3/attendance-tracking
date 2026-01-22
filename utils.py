from datetime import date, timedelta

def today():
    return date.today().isoformat();

# Return the most recent Sunday
def most_recent_sunday():
    today = date.today()
    most_recent_sunday = today - timedelta(days=(today.weekday() + 1) % 7) # sunday = 6
    return most_recent_sunday.isoformat()

def get_date_months_ago(delta_month = 3):
    today = date.today()
    date_months_ago = today - timedelta(months=delta_month)
    return date_months_ago.isoformat()