import streamlit as st
import utils

from db.database import AttendanceDB

# Connect to database
@st.cache_resource
def get_db():
    return AttendanceDB("attendance.db")

def set_page():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
            .block-container {
                padding: 1.5rem;
            }

            .block-container h5 {
                text-align: center;
                padding: 0.2rem;
                margin: 0rem;
                /* font-weight: normal; /*
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_date():
    most_recent_sunday = utils.most_recent_sunday(iso = False)
    st.markdown(
        f"""
        <h5 style="margin-bottom: 1rem;">
            {most_recent_sunday.year}年 
            {most_recent_sunday.month}月 
            {most_recent_sunday.day}日 Attendance 出席表
        </h5>
        """,
        unsafe_allow_html=True
    ) 

def display_organization():
    st.markdown(
        """<h5>The Salvation Army San Gabriel Corps 基督教救世軍洛杉磯堂</h5>""",
        unsafe_allow_html=True
    )