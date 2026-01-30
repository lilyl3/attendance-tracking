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
        columns=["Member ID", "English Name 英文名", "Chinese Name 中文名", "Present 在场吗?"]
    )
    # Present 在场吗? stores date formatted as YYYY-MM-DD => If str exists, then previously marked member as attended
    data_df["Present 在场吗?"] = data_df["Present 在场吗?"].apply(lambda x: bool(x) if pd.notna(x) else False).astype("boolean")
    # data_df = data_df.set_index("Member ID")
    # data_df = data_df.sort_values(by="English Name 英文名")

    for i, row in data_df.iterrows():
        # Create a container for each row
        with st.container(border = True, gap="xxsmall"):
            col1, col2, col3 = st.columns([1, 2, 2])    
            with col1:
                isPresent = st.checkbox(
                    label="{row['English Name 英文名']}",
                    value=row["Present 在场吗?"],
                    key=f"isPresent_{row['Member ID']}",
                    label_visibility="hidden"  # Hide the label
                )
                # Update DB if changed
                if isPresent != row["Present 在场吗?"]:
                    # print(row["Member ID"], row["English Name 英文名"], isPresent, data_df.at[i, "Present 在场吗?"])
                    if data_df.at[i, "Present 在场吗?"]:
                        db.delete_attendance(row['Member ID'])
                    else:
                        db.add_attendance(row['Member ID'])
                    data_df.at[i, "Present 在场吗?"] = isPresent
                    data_df.to_csv(file_name)

            with col2:
                st.text(row['English Name 英文名'])
            
            with col3:
                chinese_name = ""
                if row['Chinese Name 中文名'] is not None:
                    chinese_name += f"{row['Chinese Name 中文名']}"
                st.text(chinese_name)