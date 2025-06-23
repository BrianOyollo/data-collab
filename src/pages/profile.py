import streamlit as st
from sqlalchemy import text
from menu import menu
from utils import utils

conn = st.connection("sql")
utils.ensure_user_in_session(conn)

st.sidebar.markdown("# :blue[DataCollab]")
menu()
utils.display_messages()

if st.user.is_logged_in:
    if st.session_state["user"]:
        user = st.session_state["user"]

        # ==================================  PROFILE INFORMATION ============================

        def update_user_info():
            # update user info
            data = {
                "id":user['id'],
                "name":st.session_state['form_name'],
                "phone":st.session_state['form_phone'],
                "github_url":st.session_state['form_github_url'],
                "linkedin_url":st.session_state['form_linkedin_url'],
                "portfolio_url":st.session_state['form_portfolio_url']
            }
            update_user_query = text("""
                UPDATE data_collab.users
                SET name=:name,phone=:phone,github_url=:github_url,linkedin_url=:linkedin_url,portfolio_url=:portfolio_url
                WHERE id=:id;            
            """)
            try:
                with conn.session as session:
                    session.execute(update_user_query, data)
                    session.commit()
                    utils.add_session_state_msg({"text":"Profile successfully updated", "icon":":material/person_check:"})

                    # update user
                    for k,v in data.items():
                        st.session_state["user"][k] = v

                    st.rerun()
            except Exception as e:
                # log e
                raise
        
        @st.dialog("Edit Profile")
        def edit_profile():
            with st.form("Edit Profile"):
                name = st.text_input("Full Name:",value=user['name'], max_chars=100, key="form_name")
                phone = st.text_input("Phone no:",value=user['phone'], max_chars=15, key="form_phone")
                github_url = st.text_input("GitHub:",value=user['github_url'], placeholder="https://github.com/abc", key="form_github_url")
                linkedin_url = st.text_input("LinkedIn:",value=user['linkedin_url'], placeholder="https://www.linkedin.com/in/abc", key="form_linkedin_url")
                portfolio_url = st.text_input("Portfolio:",value=user['portfolio_url'], placeholder="full link to your portfolio ", key="form_portfolio_url")

                update_profile_btn = st.form_submit_button("Update")
                if update_profile_btn:
                    update_user_info()

        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="{user['profile_image']}" width="100" style="border-radius: 50%; margin-bottom: 10px;" />
                <h3 style="padding-bottom:1px;">{user['name']}</h3>
                <p>{user['email']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Profile Info", divider="grey")
        profile_data = {}
        profile_keys = ['name','phone','github_url','linkedin_url','portfolio_url']
        profile_data = {k:v for k,v in user.items() if k in profile_keys}

        st.json(profile_data)

        pi_col1,pi_col2,pi_col3 = st.columns(3)
        with pi_col2:
            edit_info_btn = st.button(
                "Edit Info", 
                icon=":material/person_edit:", 
                type="secondary", 
                use_container_width=True,
                key="btn_edit_profile_info",
            )
            if edit_info_btn:
                edit_profile()


        # ==================================  USER PROJECTS ============================
        st.subheader("Projects", divider="grey")


else:
    st.warning("You must login first to access this page")

