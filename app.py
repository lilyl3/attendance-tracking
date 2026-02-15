import streamlit as st
from config_pages import set_page
from pages import Add_Member, Dashboard, Mark_attendance

set_page()

pg = st.navigation(
    [ 
        Mark_attendance.Mark_Attendance,
        Dashboard.Dashboard,
        Add_Member.Add_Member
    ],
    position = "top"
)
pg.run()