import streamlit as st
from utils import utils
import time

conn = st.connection('sql')

st.set_page_config(
    page_title="DataCollab",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# will run on st.rerun()
if "ss_message" in st.session_state:
    message = st.session_state["ss_message"]
    if message is not None:
        st.toast(message["text"], icon=f'{message["icon"]}')
        time.sleep(4)
        st.session_state["ss_message"] = None

st.header(":blue[DataCollab]")

pages = {
    "Projects":[
        st.Page("pages/projects.py", title="Projects"),
        st.Page("pages/new_project.py", title="Create a Project"),
    ],
    "Users": [
        st.Page("pages/students.py", title="Students"),
        st.Page("pages/instructors.py", title="Instructors"),
    ],
    "Resources": [
        st.Page("pages/blogs.py", title="Blogs"),
        st.Page("pages/about.py", title="About"),
    ]
}

if st.user.is_logged_in:
    if "user" not in st.session_state:
        utils.sync_user(conn, st.user)

    pages["Account"] = [
        st.Page("pages/profile.py", title="Profile")
    ]
    with st.sidebar:
        if st.button("Logout"):
            st.logout()
else:
    with st.sidebar:
        if st.button("Login with Google"):
            st.login("google")
        

pg = st.navigation(pages)
pg.run()