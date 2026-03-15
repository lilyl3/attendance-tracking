import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime

from config_pages import set_page, display_organization, get_db
from utils import most_recent_sunday, attendance_file_paths, trend_paths
from pages import Mark_attendance

db = get_db()

def get_on_date(data_type):
    if data_type == "All Attendees":
        return db.get_attendees_on_date(st.session_state["sunday_date"])
    else:
        return db.get_new_friends(st.session_state["sunday_date"])
    
def get_on_range(data_type):
    if data_type == "All Attendees":
        return db.get_attendees_in_range(st.session_state["year"])
    else:
        return db.get_new_friends_in_range(st.session_state["year"])
    
def plot_attendance_trends(data_type, file_path):
    attendees_in_range = get_on_range(data_type)
    attendees_in_range = pd.DataFrame(
        attendees_in_range, 
        columns=["Date"]
    )
    # Count attendees per date
    counts_df = attendees_in_range['Date'].value_counts().reset_index()
    counts_df.columns = ['Date', 'Count']
    counts_df = counts_df.sort_values('Date')
    counts_df.to_csv(file_path)

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

def Dashboard():
    set_page()
    display_organization()

    # Update database
    if "marked" in st.session_state and st.session_state["marked"]:
        Mark_attendance.update_db()

    # Set session state
    if "page" not in st.session_state or st.session_state["page"] != "dashboard":
        st.session_state["page"] = "dashboard"
    if "sunday_date" not in st.session_state:
        st.session_state["sunday_date"] = most_recent_sunday(iso=False)
        st.session_state["year"] = date.today().year

    header_names = ["Sunday Overview", "Attendance Trends"]
    h1, h2 = st.tabs(header_names)

    file_paths = attendance_file_paths(st.session_state["sunday_date"])
    # Display list of attendees on date stored in session state
    with h1:
        st.date_input("Date 日期", key="sunday_date")
        tab_names = ["All Attendees", "New Friends"]
        tabs = st.tabs(tab_names)
        for i, tab in enumerate(tabs):
            with tab:
                attendees = get_on_date(tab_names[i])
                attendees = pd.DataFrame(
                    attendees, 
                    columns=["English Name 英文名", "Chinese Name 中文名"]
                )
                st.write("Total Attendees 总数: ", attendees.shape[0])
                st.dataframe(attendees, hide_index = True, height="content")
                attendees.to_csv(file_paths[i])

    # Visualize attendance trends
    trend_file_paths = trend_paths(st.session_state["year"])
    with h2:
        st.number_input(
            "Select Year",
            min_value=2000,
            max_value=2100,    
            key="year",     
            step=1             # increment step
        )
        tabs = st.tabs(tab_names)
        for i, tab in enumerate(tabs):
            with tab:
                plot_attendance_trends(tab_names[i], trend_file_paths[i])