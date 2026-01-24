import streamlit as st
from config_pages import set_page, display_organization, display_date
from app import get_db

set_page()
display_organization()
display_date()

db = get_db()
members = db.get_members()
print(members)
    