import streamlit as st
from sqlalchemy import text
from utils import utils

conn = st.connection("sql")

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

        with st.expander("Project Category(s)"):
            st.pills("The project involves", options=project_categories,selection_mode="multi", key="new_project_project_categories")
        
        with st.expander("Tech Stack"):
            st.pills("The project will use...", options=tech_stacks,selection_mode="multi", key="new_project_tech_stack")
        
        collab_status = st.radio(
            "Are you open to collaborations?",
            options=["Yes", "Maybe Later"],
            captions=["", "Selected collaborations below won't be saved"],
            horizontal=True,
            key="new_project_collab_status"
        )
        with st.expander("Collaborations"):
            desired_roles = st.pills("Looking to collaborate with...", options=roles,selection_mode="multi", key="new_project_desired_roles")

        github_url = st.text_input("GitHub link", key="new_project_github_link")
        create_project = st.form_submit_button("Create")
        return create_project

if st.user.is_logged_in:
    create_project = create_project_form()
    if create_project:
        utils.create_project(conn)
        st.switch_page("pages/projects.py")
        
else:
    st.warning("You must login first to create a project")


