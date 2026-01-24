import streamlit as st
from config_pages import set_page, display_organization
from app import get_db

db = get_db()

# Only initialize page once per session
if "page" not in st.session_state or st.session_state["page"] != "add_member_page":
    set_page()
    display_organization()
    st.subheader("Add Member", divider="red")

    with st.form(key = "add_member_form", clear_on_submit=True):
        english_name = st.text_input("English Name 英文名")
        chinese_name = st.text_input("Chinese Name 中文名")
        submitted = st.form_submit_button("Enter")

        if submitted:
            db.add_member(english_name, chinese_name)
            st.success("Member added! 已加成员!")

    st.session_state["page"] = "add_member_page"