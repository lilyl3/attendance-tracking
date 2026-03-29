import streamlit as st

from config_pages import set_page, display_organization, get_db
from pages import Add_Member

db = get_db()

def View_Member():
    set_page()
    display_organization()

    st.session_state["page"] = "view_members"

    family_initial = st.selectbox(
        "Family Initial 姓氏首字母",
        (c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    )

    if family_initial:
        options = db.get_members_with_family_initial(family_initial)
        options = [None] + [o[0] for o in options if o[0] is not None]
        member = st.selectbox(
            "Select a member to edit",
            options
        )

        if member:
            member_id = int(member.split('.')[0])
            member_data = db.get_member_info(member_id)
            member_form(member_id, member_data)

vnames = [
    'id', 'english_name', 'chinese_name', 'gender', 'age', 'phone_number', \
    'address', 'language', 'visit_purpose', 'faith_status', 'family_id'
]
vnameIdx = {vname: i for i, vname in enumerate(vnames)}

def member_form(member_id, member_data):
      
    lname, fname = member_data[vnameIdx["english_name"]].split(",")
    with st.form(key="update_member_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            last_name = st.text_input("Last Name 英文姓氏", value = lname)
        with col2:
            first_name = st.text_input("First Name 英文名字", value = fname)
        chinese_name = st.text_input("Chinese Name 中文名", value = member_data[vnameIdx["chinese_name"]])

        gender_options = ["Male 男", "Female 女"]
        gender = st.radio(
            "Gender 性别", 
            gender_options, 
            index = gender_options.index(member_data[vnameIdx["gender"]]) if member_data[vnameIdx["gender"]] else 0
        )
        age_options = ["Prefer not to say 不愿说", "0-12", "13-18", "19-30", "31-59", "60+"]
        age = st.radio(
            "Age 年龄", 
            age_options, 
            index = age_options.index(member_data[vnameIdx["age"]]) if member_data[vnameIdx["age"]] else 0
        )
        phone_number = st.text_input(
            "Phone Number 电话号码", 
            value = "" if not member_data[vnameIdx["phone_number"]] else member_data[vnameIdx["phone_number"]]
        )
        address = st.text_input(
            "Address 地址",
            value = "" if not member_data[vnameIdx["address"]] else member_data[vnameIdx["address"]]
        )
        language = st.multiselect(
            "Language 语言", 
            ["English 英语", "Mandarin 国语", "Cantonese 粤语"],
            default = ["English 英语"] if not member_data[vnameIdx["language"]] else member_data[vnameIdx["language"]].split(", ")
        )
        faith_options = ["Interested in becoming a Christian 有兴趣成为基督徒", "Christian 基督徒", "Other 非基督徒"]
        faith_status = st.radio(
            "Faith 信仰", 
            faith_options,
            index = faith_options.index(member_data[vnameIdx["faith_status"]]) if member_data[vnameIdx["faith_status"]] else 0
        )

        Add_Member.style_button()
        save_button = st.form_submit_button("Update member 保存")
        if save_button:
            
            if (last_name and first_name) or chinese_name:
                db.update_member_info([
                    f"{last_name}, {first_name}", 
                    chinese_name, 
                    gender, 
                    age, 
                    phone_number, 
                    address, 
                    ", ".join(language), 
                    faith_status, 
                    member_id
                ])

                st.success("Member updated! 更新成功!")
                st.rerun()
            else:
                st.warning("Name: Required 姓名：必填")