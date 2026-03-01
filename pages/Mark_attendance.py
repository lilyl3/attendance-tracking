import streamlit as st
import pandas as pd
import time
import os as os

from config_pages import set_page, display_organization, display_date, get_db
from utils import attendance_file_path

file_path = attendance_file_path()
# -----------------------------------------------------------
#                 Load DB connection
# -----------------------------------------------------------
db = get_db()

def update_db():
    if not st.session_state["marked"]:
        return
    
    i, member_id, isPresent = st.session_state["marked"]
    # print("Updated member=", member_id, isPresent)
    if isPresent:
        db.add_attendance(member_id)
    else:
        db.delete_attendance(member_id)
    st.session_state["mask"][i] = st.session_state["updated_mask"][i]
    st.session_state["marked"] = None

def Mark_Attendance():
    set_page()
    display_organization()
    display_date()
    
    if "marked" in st.session_state:
        update_db()
    else:
        st.session_state["marked"] = None

    # -----------------------------------------------------------
    #               Load data once into session
    # -----------------------------------------------------------
    if "page" not in st.session_state or st.session_state["page"] != "mark_attendance":
        print("reset")
        st.session_state["page"] = "mark_attendance"

        data = db.get_members()
        data_df = pd.DataFrame(
            data,
            columns=["Member ID", "Family Name", "Family ID", "English Name 英文名", "Chinese Name 中文名", "Present 在场吗?"]
        )
        data_df = data_df.set_index("Member ID")
        data_df["Present 在场吗?"] = data_df["Present 在场吗?"].apply(
            lambda x: bool(x) if pd.notna(x) else False
        ).astype("boolean")
        # Sort by family name, family id
        data_df.sort_values(by=["Family Name", "Family ID"], inplace=True)

        # -----------------------------------------------------------
        #                           Styling
        # -----------------------------------------------------------
        family_ids = data_df["Family ID"].unique()
        st.session_state["family_info"] = dict()
        # family_info[id][0] = color index
        # family_info[id][1] = total count of people in family id
        for i, id in enumerate(family_ids):
            st.session_state["family_info"][id] = (i % 2, sum(data_df["Family ID"] == id))

        # -----------------------------------------------------------
        #    Split dataframe, each subsections displayed in a tab
        # -----------------------------------------------------------
        st.session_state["db"] = []
        st.session_state["mask"] = []
        st.session_state["tab_names"] = []

        start_index = 0
        total = 0

        # Generate tab names
        def get_tab_name(tab_df):
            first_family = tab_df.iloc[0]["Family Name"]
            last_family = tab_df.iloc[-1]["Family Name"]
            return f"{first_family}-{last_family}"

        # Find tab boundaries
        for id in family_ids:
            family_size = st.session_state["family_info"][id][1]
            # If adding this family exceeds 30, start a new range before adding this family
            if total + family_size > 30:
                end_index = start_index + total
                st.session_state["db"].append(data_df.iloc[start_index:end_index])
                st.session_state["mask"].append(st.session_state["db"][-1]["Present 在场吗?"])
                st.session_state["tab_names"].append(get_tab_name(st.session_state["db"][-1]))

                start_index = start_index + total
                total = 0
            total += family_size
        # Add the final range
        st.session_state["db"].append(data_df.iloc[start_index:start_index + total])
        st.session_state["mask"].append(st.session_state["db"][-1]["Present 在场吗?"])
        st.session_state["tab_names"].append(get_tab_name(st.session_state["db"][-1]))

        st.session_state["updated_mask"] = [s.copy() for s in st.session_state["mask"]]

    colors = ["#ffffff", "#f0f8ff"]
    def color_by_family(row):
        index = st.session_state["family_info"][row['Family ID']][0]
        return [f"background-color: {colors[index]}"] * len(row)
    
    # -----------------------------------------------------------
    #            Display <= 30 persons per tab
    # -----------------------------------------------------------
    tabs = st.tabs(st.session_state["tab_names"])
    for i, tab in enumerate(tabs):
        with tab:
            edited_df = st.data_editor(
                st.session_state["db"][i].style.apply(color_by_family, axis=1),
                column_config={
                    "Family Name": None,
                    "Family ID": None,
                    "Present 在场吗?": st.column_config.CheckboxColumn("Present 在场吗?")
                },
                disabled=["English Name 英文名", "Chinese Name 中文名"],
                hide_index=True,
                height="content"
            )

            # -----------------------------------------------------------
            #                 Auto-save changes on every edit
            # -----------------------------------------------------------
            st.session_state["updated_mask"][i] = edited_df["Present 在场吗?"]
            mask = edited_df["Present 在场吗?"] != st.session_state["mask"][i]

            if mask.any():         
                member_id = int(edited_df[mask].index[0])
                print(f"Todo: update member={member_id}, {edited_df.loc[member_id, 'English Name 英文名']} to {edited_df.loc[member_id, 'Present 在场吗?']}")
                st.session_state["marked"] = (i, member_id, edited_df.loc[member_id, "Present 在场吗?"])