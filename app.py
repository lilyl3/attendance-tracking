import streamlit as st
from config_pages import set_page

set_page()

pg = st.navigation(
    ["pages/Dashboard.py", "pages/Mark_attendance.py"],
    position = "top"
)
pg.run()