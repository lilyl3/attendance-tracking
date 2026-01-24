import streamlit as st
from config_pages import set_page, display_organization
from db.database import AttendanceDB

# Connect to database
@st.cache_resource
def get_db():
    return AttendanceDB("attendance.db")

set_page()

pg = st.navigation(
    ["pages/Dashboard.py", "pages/Mark_attendance.py", "pages/Add_Member.py"],
    position = "top"
)
pg.run()