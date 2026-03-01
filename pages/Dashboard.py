import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from config_pages import set_page, display_organization, get_db
from utils import most_recent_sunday, get_date_months_ago, format_date
from pages import Mark_attendance

def Dashboard():
    set_page()
    display_organization()
    db = get_db()

    # ---------------- Update database  ---------------------
    if "marked" in st.session_state and st.session_state["marked"]:
        Mark_attendance.update_db()

    # ---------------- Set session state ---------------------
    if "page" not in st.session_state or st.session_state["page"] != "dashboard":
        st.session_state["page"] = "dashboard"

    if "sunday_date" not in st.session_state:
        st.session_state["sunday_date"] = most_recent_sunday(iso=False)
    if "start_date" not in st.session_state:
        st.session_state["start_date"] = get_date_months_ago(delta_month = 3, iso = False)
    if "end_date" not in st.session_state:
        st.session_state["end_date"] = most_recent_sunday(iso=False)

    st.subheader("Sunday Overview", divider="blue")

    # ------------------------------------------------------------
    #                   Display Sunday attendance
    # ------------------------------------------------------------
    placeholder = st.empty() # Empty container
    # Function to dynamically render the date input using the session state
    def render_date_input():
        return placeholder.date_input(
            "Date 日期",
            value=st.session_state["sunday_date"]
        )
    sunday_date = render_date_input() # Returns value

    attendees = db.get_attendees_on_date(sunday_date)
    attendees = pd.DataFrame(
        attendees, 
        columns=["English Name 英文名", "Chinese Name 中文名"]
    )
    st.write("Total Attendees 总数: ", attendees.shape[0])
    st.dataframe(attendees, hide_index = True, height="content")

    # ------------------------------------------------------------
    #               Visualize attendance trends
    # ------------------------------------------------------------
    st.subheader("Attendance Trends", divider="blue")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start date",
            key = "start_date"
        )
    with col2:
        end_date = st.date_input(
            "End date",
            key = "end_date"
        )
    attendees_in_range = db.get_attendees_in_date_range(
        start_date=st.session_state["start_date"],
        end_date=st.session_state["end_date"]
    )
    attendees_in_range = pd.DataFrame(
        attendees_in_range, 
        columns=["Date"]
    )
    # Count attendees per date
    counts_df = attendees_in_range['Date'].value_counts().reset_index()
    counts_df.columns = ['Date', 'Count']
    counts_df = counts_df.sort_values('Date')

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