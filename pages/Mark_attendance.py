import streamlit as st
import pandas as pd
import numpy as np
import os

from config_pages import set_page, display_organization, display_date
from app import get_db
from utils import most_recent_sunday

file_name = "attendance/" + most_recent_sunday() + ".csv"
    
set_page()
display_organization()
display_date()

db = get_db()
data = db.get_members()
data_df = pd.DataFrame(
    data,
    columns=["MemberID", "English Name", "Chinese Name", "Present?"]
)
# Present? stores date formatted as YYYY-MM-DD => If str exists, then previously marked member as attended
data_df["Present?"] = data_df["Present?"].apply(lambda x: bool(x) if pd.notna(x) else False).astype("boolean")
data_df = data_df.set_index("MemberID")
data_df = data_df.sort_values(by="English Name")

edited_df = st.data_editor(
    data_df,
    column_config={
        "Present?": st.column_config.CheckboxColumn(
            "Present?",
            default=False,
        )
    },
    disabled=["English Name", "Chinese Name"],
    hide_index=True,
)

edited_df.to_csv(file_name)
# Update database
# print("****")
# print(data_df)
# print(edited_df)
mask = edited_df["Present?"] != data_df["Present?"]
if (mask.any()):
    member_id = int(edited_df[mask].index[0])
    if edited_df.loc[member_id, "Present?"]:
        # print("Marked", edited_df.loc[member_id, "English Name"], "as present")
        db.add_attendance(member_id)
    else:
        # print("Marked", edited_df.loc[member_id, "English Name"], "as absent")
        db.delete_attendance(member_id)
# print("****")