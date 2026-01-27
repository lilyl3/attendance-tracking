import streamlit as st
from config_pages import set_page
from pages import Add_Member, Dashboard, Mark_attendance

set_page()

pg = st.navigation(
    [
        Dashboard.Dashboard, 
        Mark_attendance.Mark_Attendance,
        Add_Member.Add_Member
    ],
    position = "top"
)
pg.run()