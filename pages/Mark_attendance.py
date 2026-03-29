import streamlit as st
import pandas as pd
import os as os

from config_pages import set_page, display_organization, get_db
from utils import most_recent_sunday

def style_tabs():
    st.markdown("""
            <style>
                button[role="tab"] {
                    padding: 5px 15px;
                }
            </style>
        """, unsafe_allow_html=True)

# Update attendance table in database
def update_db():
    if not st.session_state["marked"]:
        return
    
    i, member_id, isPresent, att_date = st.session_state["marked"]
    if isPresent:
        db.add_attendance(member_id, att_date)
    else:
        db.delete_attendance(member_id, att_date)
    st.session_state["mask"][i] = st.session_state["updated_mask"][i]
    st.session_state["marked"] = None

# Update session state to indicate date has changed
# So attendance data will be reloaded from the db
def attendance_updated_att_date():
    st.session_state["updated_att_date"] = True

# Returns Pandas dataframe of attendance data
# specified by session state "att_date"
# sorted in order by Family Name, Family ID
def load_attendance_data():
    if "att_date" not in st.session_state:
        return pd.DataFrame()
    
    data = db.get_members(sunday_date=st.session_state["att_date"])
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
    return data_df

# Sets key "family_info" in session_state
# to a dict mapping every family to a color id for styling
# such that adjacent families have alternate colors
def map_family_to_color(data_df):
    family_ids = data_df["Family ID"].unique()
    st.session_state["family_info"] = dict()
    # family_info[id][0] = color index
    # family_info[id][1] = total count of people in family id
    for i, id in enumerate(family_ids):
        st.session_state["family_info"][id] = (i % 2, sum(data_df["Family ID"] == id))

# Sets key "tabs" in session_state
# up  session state such that attendance data is 
# split by A-Z based on the first character of a family name
def split_attendance_by_tabs(data_df):
    st.session_state["db"] = []
    st.session_state["mask"] = []
    st.session_state["tab_names"] = []

    for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        mask = data_df["Family Name"].str.startswith(c)
        if mask.any():
            st.session_state["tab_names"].append(c)
            st.session_state["db"].append(
                data_df[data_df["Family Name"].str.startswith(c)]
            )
            st.session_state["mask"].append(
                st.session_state["db"][-1]["Present 在场吗?"]
            )
    st.session_state["updated_mask"] = [s.copy() for s in st.session_state["mask"]]

def reset_data():
    data_df = load_attendance_data()
    map_family_to_color(data_df)
    split_attendance_by_tabs(data_df)

def setup_session_state():
    if "att_date" not in st.session_state:
        st.session_state["att_date"] = most_recent_sunday(iso=False)
        st.session_state["updated_att_date"] = False

    if "page" not in st.session_state or st.session_state["page"] != "mark_attendance":
        st.session_state["page"] = "mark_attendance"
        reset_data()
        
    if st.session_state["updated_att_date"]:
        st.session_state["updated_att_date"] = False    
        reset_data()

    if "marked" in st.session_state:
        update_db()
    else:
        st.session_state["marked"] = None

# -----------------------------------------------------------
#                 Load DB connection
# -----------------------------------------------------------
db = get_db()

def Mark_Attendance():
    set_page()
    display_organization()
    setup_session_state()

    st.date_input(
        "Date 日期",
        key="att_date", 
        on_change=attendance_updated_att_date)

    # Assign color to family for styling
    colors = ["#ffffff", "#f0f8ff"]
    def color_by_family(row):
        index = st.session_state["family_info"][row['Family ID']][0]
        return [f"background-color: {colors[index]}"] * len(row)

    style_tabs()
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

            rows = edited_df[mask]
            if not rows.empty:
                member_id = int(rows.index[0])   
                st.session_state["marked"] = (i, member_id, edited_df.loc[member_id, "Present 在场吗?"], st.session_state["att_date"])
                print(st.session_state["marked"])