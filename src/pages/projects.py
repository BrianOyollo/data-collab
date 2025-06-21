import streamlit as st
from html import escape

from utils import utils

conn = st.connection("sql")

projects = [row._mapping for row in utils.fetch_projects(conn)]
st.subheader(f"Projects({len(projects)})")


for project in projects:
   with st.container(border=True, key=f"cont_{project['id']}"):
        st.html(f"<h5 style='margin:0'>{project['title']}</h5>")
        st.html(f"<small>{project['description']}</small>")

        tech_stack_items = " • ".join(str(item) for item in project.get('tech_stack') or [] if item)
        desired_roles_items = " • ".join(str(item) for item in project.get("desired_roles") or [] if item)
        categories = " • ".join(str(item) for item in project.get('categories') or [] if item)

        tech_stack, desired_roles, project_category = st.tabs(["Tech Stack","Looking to collab with","Project Categories"])
        with tech_stack:
            st.markdown(f"<small style='margin:0'>{tech_stack_items}</small>", unsafe_allow_html=True)

        with desired_roles:
            st.markdown(f"<small style='margin:0'>{desired_roles_items}</small>", unsafe_allow_html=True)

        with project_category:
            st.markdown(f"<small style='margin:0'>{categories}</small>", unsafe_allow_html=True)


        # projet github link
        project_link = f"[GitHub](project['github_url'])"

        # collab status
        collab_status = collab_status = "green-badge[:material/handshake: Open to Collab]"
        if not project['is_open_to_collab']:
            collab_status = "grey-badge[:material/handshake: Closed to Collab]"

        st.markdown(
            f"""
            :violet-badge[:material/deployed_code_account: {project['owner']}] 
            :blue-badge[:material/fork_right: {project_link}] 
            :{collab_status}
            :orange-badge[:material/groups: Current Members: {project['collaborators']}] 
            """

        )
        st.write("")
        btn1,btn2,btn3 = st.columns(3)
        with btn1:
            st.button("Leave Project",type="tertiary", icon=":material/door_open:", use_container_width=True,key=f"leave_project_btn_{project['id']}")
        with btn2:
            if project['is_open_to_collab']:
                join_project_btn = st.button("Join Project", type="tertiary", icon=":material/rocket_launch:", use_container_width=True, key=f"btn_{project['id']}")
                if join_project_btn:
                    project_id = project['id']
                    user_id = st.session_state["user"]["id"]
                    utils.join_project(conn, project_id, user_id)
        with btn3:
            if project["email"] == st.session_state["user"]["email"]:
                st.button("Delete Project",type="tertiary", icon=":material/delete:", use_container_width=True, key=f"dlt_btn_{project['id']}")
    