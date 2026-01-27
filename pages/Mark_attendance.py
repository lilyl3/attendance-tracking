import streamlit as st
import pandas as pd

from config_pages import set_page, display_organization, display_date, get_db
from utils import most_recent_sunday

file_name = "sunday_attendance/" + most_recent_sunday() + ".csv"

def Mark_Attendance():
    set_page()
    display_organization()
    display_date()

    db = get_db()
    data = db.get_members()
    data_df = pd.DataFrame(
        data,
        columns=["MemberID", "English Name 英文名", "Chinese Name 中文名", "Present 在场吗?"]
    )
    # Present 在场吗? stores date formatted as YYYY-MM-DD => If str exists, then previously marked member as attended
    data_df["Present 在场吗?"] = data_df["Present 在场吗?"].apply(lambda x: bool(x) if pd.notna(x) else False).astype("boolean")
    data_df = data_df.set_index("MemberID")
    data_df = data_df.sort_values(by="English Name 英文名")

    edited_df = st.data_editor(
        data_df,
        column_config={
            "Present 在场吗?": st.column_config.CheckboxColumn(
                "Present 在场吗?",
                default=False,
            )
        },
        disabled=["English Name 英文名", "Chinese Name 中文名"],
        hide_index=True,
    )

    edited_df.to_csv(file_name)
    # Update database
    # print("****")
    # print(data_df)
    # print(edited_df)
    mask = edited_df["Present 在场吗?"] != data_df["Present 在场吗?"]
    if (mask.any()):
        member_id = int(edited_df[mask].index[0])
        if edited_df.loc[member_id, "Present 在场吗?"]:
            # print("Marked", edited_df.loc[member_id, "English Name 英文名"], "as present")
            db.add_attendance(member_id)
        else:
            # print("Marked", edited_df.loc[member_id, "English Name 英文名"], "as absent")
            db.delete_attendance(member_id)
    # print("****")