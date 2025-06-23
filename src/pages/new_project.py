import streamlit as st
from sqlalchemy import text
from utils import utils
from menu import menu

conn = st.connection("sql")

utils.display_messages()
utils.ensure_user_in_session(conn)

st.sidebar.markdown("# :blue[DataCollab]")
menu()


st.subheader("New Project")

def create_project_form():
    project_categories = []
    tech_stack = []
    roles = []
    with conn.session as session:
        # tech stacks
        project_categories_results = session.execute(text("SELECT name FROM data_collab.categories")).fetchall()
        project_categories = [row[0] for row in project_categories_results]

        # tech stacks
        tech_stack_results = session.execute(text("SELECT name FROM data_collab.tech_stack")).fetchall()
        tech_stacks = [row[0] for row in tech_stack_results]

        # desired collaborations
        roles_results = session.execute(text("SELECT name FROM data_collab.roles")).fetchall()
        roles = [row[0] for row in roles_results]

    with st.form("New Project"):
        title = st.text_input("Title:", key="new_project_project_title")
        description = st.text_area("Description", key="new_project_project_description")

        project_categories = st.multiselect(
            "Project Category(s)", 
            options=project_categories,
            placeholder="AI, data engineering, frontend development,...", 
            key="new_project_project_categories"
        )

        tech_stack = st.multiselect(
            "Tech Stack", 
            options=tech_stacks,
            placeholder="python, sql, excel,...", key="new_project_tech_stack")
        
        collab_status = st.radio(
            "Are you open to collaborations?",
            options=["Yes", "Maybe Later"],
            captions=["", "Selected collaborations below won't be saved"],
            horizontal=True,
            key="new_project_collab_status"
        )

        desired_roles = st.multiselect(
            "Collaborations", 
            options=roles, 
            placeholder="pick the roles you want to collaborate with", 
            key="new_project_desired_roles"
        )

        github_url = st.text_input("GitHub link", 
            placeholder="https://github.com/janedoe", 
            label_visibility="visible",
            help="Please enter a full GitHub url",
            key="new_project_github_link"
        )
        create_project = st.form_submit_button("Create")
        return create_project

if st.user.is_logged_in:
    new_project = create_project_form()
    if new_project:
        utils.create_project(conn)
        utils.add_session_state_msg({
            "text":":green[Project successfully created]",
            "icon":":material/celebration:"
        })
        st.switch_page("pages/projects.py")
        
else:
    utils.add_session_state_msg({
            "text":":red[You must login first to add a project]",
            "icon":":material/error:"
    })
    st.switch_page("pages/login.py")


