import streamlit as st
from html import escape

from utils import utils

conn = st.connection("sql")

projects = [row._mapping for row in utils.fetch_projects(conn)]
st.subheader(f"Projects({len(projects)})")
comments_data = [
    {
        "name": "Brian",
        "message": "Hey, nice project. I want in",
        "time": "8.46pm"
    },
    {
        "name": "Aisha",
        "message": "This looks promising. Do you still need a frontend developer?",
        "time": "9.02pm"
    },
    {
        "name": "Kelvin",
        "message": "I'm interested in the data analysis part. Let me know how I can contribute.",
        "time": "9.15pm"
    },
    {
        "name": "Chloe",
        "message": "Impressive work so far! Can I join as a designer?",
        "time": "9.30pm"
    },
    {
        "name": "David",
        "message": "Would love to collaborate. I'm good with backend systems.",
        "time": "9.42pm"
    },
    {
        "name": "Emily",
        "message": "Count me in! I'm working on something similar.",
        "time": "10.05pm"
    },
    {
        "name": "Sam",
        "message": "Great concept! Can I help with data visualization?",
        "time": "10.18pm"
    },
    {
        "name": "Njeri",
        "message": "Hey, this aligns with my interests. Let's collaborate!",
        "time": "10.33pm"
    },
    {
        "name": "Ali",
        "message": "Looks exciting. I can help with testing and QA.",
        "time": "10.45pm"
    },
    {
        "name": "Zainab",
        "message": "Very cool project. I'm available for weekend contributions.",
        "time": "11.00pm"
    },
    {
        "name": "Omondi",
        "message": "I've got experience with geodata. Happy to join in!",
        "time": "11.12pm"
    }
]



for project in projects:
   with st.container(border=True, key=f"cont_{project['id']}"):
        st.html(f"<h5 style='margin:0'>{project['title']}</h5>")
        st.html(f"<small>{project['description']}</small>")

        

        tech_stack_items = " • ".join(str(item) for item in project.get('tech_stack') or [] if item)
        desired_roles_items = " • ".join(str(item) for item in project.get("desired_roles") or [] if item)
        categories = " • ".join(str(item) for item in project.get('categories') or [] if item)

        tech_stack, desired_roles, project_category = st.tabs(["Tech Stack","Desired Roles","Project Categories"])
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
            :orange-badge[:material/groups: Current Members{project['collaborators']}] 
            """

        )

        btn1,btn2,btn3 = st.columns(3)
        with btn2:
            if project['is_open_to_collab']:
                st.button("Join Project", type="tertiary", icon=":material/rocket_launch:", use_container_width=True, key=f"btn_{project['id']}")