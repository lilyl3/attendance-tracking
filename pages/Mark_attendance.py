import streamlit as st
from config_pages import set_page, display_organization, display_date

set_page()
display_organization()
display_date()

if "page" not in st.session_state or st.session_state["page"] != "mark_attendance":
    st.session_state["page"] = "mark_attendance"