import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

from config_pages import set_page
from pages import Add_Member, Dashboard, Mark_attendance, View_Member

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
    if st.session_state.get("authentication_status"):
        set_page()
        pg = st.navigation(
            [ 
                Mark_attendance.Mark_Attendance,
                Add_Member.Add_Member,
                Dashboard.Dashboard,
                View_Member.View_Member
            ],
            position="top"
        )
        pg.run()
    elif st.session_state.get('authentication_status') is False:
        st.error('Username or password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')
except Exception as e:
    st.error(e)