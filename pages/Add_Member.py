import streamlit as st
import time

from config_pages import set_page, display_organization, get_db
from utils import most_recent_sunday

def reset_all():
    st.session_state["family"] = []
    st.session_state["family_name"] = ""
    st.session_state["family_id"] = ""
    st.session_state["invited_by"] = ""

def Add_Member():
    db = get_db()

    set_page()
    display_organization()

    if "page" not in st.session_state or st.session_state["page"] != "add_member":
        st.session_state["page"] = "add_member"
        st.session_state["family"] = []
        st.session_state["family_name"] = ""
        st.session_state["family_id"] = ""
        st.session_state["invited_by"] = ""
        
    st.header("Register 登记", divider="blue")
    # -------------------------
    # No family name recorded
    # -------------------------
    st.text_input("Family Name 姓氏", key = "family_name")
    st.text_input("Invited by 邀请人", key="invited_by")

    if not st.session_state["family_id"]:
        if st.button("Save 存家庭信息") and st.session_state["family_name"]:
            # Add family to database
            family_id = db.add_family(
                st.session_state["family_name"], 
                most_recent_sunday(), 
                st.session_state["invited_by"]
            )
            st.session_state["family_id"] = family_id
            st.rerun()

    if st.session_state["family_id"]:
        # -------------------------
        # Show added members
        # -------------------------
        st.write("Members 成员")
        for i, m in enumerate(st.session_state["family"]):
            st.write(f"{i+1}. {m[0]} {m[1]}")

        st.button("Reset 重置", on_click=reset_all)

        st.subheader("Add Member 加成员", divider="blue")
        with st.form(key="add_member_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                last_name = st.text_input("Last Name 英文姓氏", value = st.session_state["family_name"])
            with col2:
                first_name = st.text_input("First Name 英文名字")
            chinese_name = st.text_input("Chinese Name 中文名")

            gender = st.radio("Gender 性别", ["Male 男", "Female 女"])
            age = st.radio("Age 年龄", ["Prefer not to say 不愿说", "0-12", "13-18", "19-30", "31-59", "60+"])

            phone_number = st.text_input("Phone Number 电话号码")
            address = st.text_input("Address 地址")

            language = st.radio("Language 语言", ["English 英语", "Mandarin 普通话", "Cantonese 粤语"])
            purpose_of_visit = st.radio("I am 我是", ["Visitor 访客", "New Resident 新居民"])
            faith_status = st.radio(
                "I am 我是", ["Interested in becoming a Christian 有兴趣成为基督徒", "Christian 基督徒", "Other 非基督徒"]
            )

            add_member_button = st.form_submit_button("Add member 加成员")
            if add_member_button:
                # Required: English or Chinese name
                if (last_name and first_name) or chinese_name:
                    member_id = db.add_member([
                        f"{last_name}, {first_name}", chinese_name, 
                        gender, age, phone_number, address, 
                        language, purpose_of_visit, 
                        faith_status, st.session_state["family_id"]
                    ])
                    db.add_attendance(member_id)

                    if not last_name:
                        last_name = ""
                    if not first_name:
                        first_name = ""
                    if not chinese_name:
                        chinese_name = ""
                    st.session_state["family"].append([f"{last_name}, {first_name}", chinese_name])

                    st.success("Member added! 已加成员!")
                    st.rerun()
                else:
                    st.warning("Name: Required 姓名：必填")