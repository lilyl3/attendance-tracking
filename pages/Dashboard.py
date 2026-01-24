import streamlit as st
from config_pages import set_page, display_organization

set_page()
display_organization()

if "page" not in st.session_state or st.session_state["page"] != "dashboard":
    st.session_state["page"] = "dashboard"