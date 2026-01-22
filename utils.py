from datetime import date, timedelta

# Return the most recent Sunday
def most_recent_Sunday():
    today = date.today()
    most_recent_sunday = today - timedelta(days=(today.weekday() + 1) % 7) # sunday = 6
    return most_recent_sunday