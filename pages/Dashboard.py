import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from app import get_db
from config_pages import set_page, display_organization
from utils import most_recent_sunday, get_date_months_ago

set_page()
display_organization()
db = get_db()

if "sunday_date" not in st.session_state:
    st.session_state["sunday_date"] = most_recent_sunday(iso=False)
    st.session_state["date_range"] = (
        get_date_months_ago(delta_month = 3, iso = False),
        most_recent_sunday(iso=False)
    )

st.subheader("Sunday Overview", divider="red")

placeholder = st.empty() # Empty container
# Function to dynamically render the date input using the session state
def render_date_input():
    return placeholder.date_input(
        "Date 日期",
        value=st.session_state["sunday_date"]
    )
sunday_date = render_date_input() # Returns value

# print("sunday_date=", sunday_date, type(sunday_date))
attendees = db.get_attendees_on_date(sunday_date)
attendees = pd.DataFrame(
    attendees, 
    columns=["English Name 英文名", "Chinese Name 中文名"]
)
st.write("Total Attendees 总数: ", attendees.shape[0])
st.dataframe(attendees, hide_index = True)

st.subheader("Attendance Trends", divider="red")
# print("date_range=", st.session_state["date_range"])
date_range = st.date_input(
    "Select date range 选择日期范围",
    value=st.session_state["date_range"]
)

attendees_in_range = db.get_attendees_in_date_range(
    start_date=st.session_state["date_range"][0],
    end_date=st.session_state["date_range"][1]
)
attendees_in_range = pd.DataFrame(
    attendees_in_range, 
    columns=["Date"]
)
# Count attendees per date
counts_df = attendees_in_range['Date'].value_counts().reset_index()
counts_df.columns = ['Date', 'Count']
counts_df = counts_df.sort_values('Date')
# print(counts_df)

fig = px.line(
    counts_df,
    x="Date",
    y="Count",
    markers=True,
    hover_data=["Date", "Count"]
)
fig.update_traces(marker=dict(size=12))

event = st.plotly_chart(
    fig, 
    selection_mode="points",
    on_select="rerun" # Returns the selection data as a dictionary
)
if len(event.selection["points"]) > 0:
    st.session_state["sunday_date"] = datetime.fromisoformat(event.selection["points"][0]['x'])
    # print("reset date to:", st.session_state["sunday_date"])