import streamlit as st
from utils import utils
import menu as menu
import time

conn = st.connection("sql")
utils.ensure_user_in_session(conn)


# will run on st.rerun()
if "ss_message" in st.session_state:
    message = st.session_state["ss_message"]
    if message is not None:
        st.toast(message["text"], icon=f'{message["icon"]}')
        time.sleep(4)
        del st.session_state["ss_message"]

st.sidebar.markdown("# :blue[DataCollab]")
with st.sidebar:
    st.page_link("app.py", label="Back to main menu", icon=":material/arrow_left_alt:")
    menu.projects_menu()
    st.write("Filters")

with st.spinner("Fetching projects...", show_time=True):
    project_results = utils.fetch_projects(conn)

if project_results is not None:
    projects = [row._mapping for row in project_results]
    st.subheader(f"Projects({len(projects)})")


    for project in projects:
        utils.project_fragement(conn,project)
        

else:
    st.subheader(f"Projects()")
    st.info("There are no projects to display right now")