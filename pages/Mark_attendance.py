import streamlit as st
import pandas as pd
import time

from config_pages import set_page, display_organization, display_date, get_db
from utils import most_recent_sunday

file_name = "sunday_attendance/" + most_recent_sunday() + ".csv"
# -----------------------------------------------------------
#                 Load DB connection
# -----------------------------------------------------------
db = get_db()

def update_db():
    for member_id, isPresent in st.session_state["marked"].items():
        # print("Updated member=", member_id, isPresent)
        if isPresent:
            db.add_attendance(member_id)
        else:
            db.delete_attendance(member_id)
    st.session_state["mask"] = st.session_state["updated_mask"]
    st.session_state["marked"] = {}

def Mark_Attendance():
    set_page()
    display_organization()
    display_date()
    
    if "marked" in st.session_state:
        update_db()
    else:
        st.session_state["marked"] = {}

    # -----------------------------------------------------------
    #               Load data once into session
    # -----------------------------------------------------------
    if "page" not in st.session_state or st.session_state["page"] != "mark_attendance":
        st.session_state["page"] = "mark_attendance"

        data = db.get_members()
        data_df = pd.DataFrame(
            data,
            columns=["Member ID", "English Name 英文名", "Chinese Name 中文名", "Present 在场吗?"]
        )

        data_df["Present 在场吗?"] = data_df["Present 在场吗?"].apply(
            lambda x: bool(x) if pd.notna(x) else False
        ).astype("boolean")

        data_df = data_df.set_index("Member ID")
        st.session_state["db"] = data_df.copy()
        st.session_state["mask"] = data_df["Present 在场吗?"]
        st.session_state["updated_mask"] = data_df["Present 在场吗?"]
        
    # -----------------------------------------------------------
    #                       Display data editor
    # -----------------------------------------------------------
    edited_df = st.data_editor(
        st.session_state["db"],
        column_config={
            "Present 在场吗?": st.column_config.CheckboxColumn("Present 在场吗?")
        },
        disabled=["English Name 英文名", "Chinese Name 中文名"],
        hide_index=True,
        height="content"
    )

    # -----------------------------------------------------------
    #                 Auto-save changes on every edit
    # -----------------------------------------------------------
    edited_df.to_csv(file_name, index=True)
    st.session_state["updated_mask"] = edited_df["Present 在场吗?"]
    mask = edited_df["Present 在场吗?"] != st.session_state["mask"]

    if mask.any():
        for member_id, row in edited_df[mask].iterrows():
            member_id = int(member_id)
            st.session_state["marked"][member_id] = row["Present 在场吗?"]
            # print("TODO: update member=", member_id, row["English Name 英文名"])

        # Save to CSV
        edited_df.to_csv(file_name, index=True)