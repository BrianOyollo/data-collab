import streamlit as st
from utils import utils
from menu import menu
import time

conn = st.connection('sql')

st.set_page_config(
    page_title="DataCollab",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)



# will run on st.rerun()
utils.display_messages()
utils.ensure_user_in_session(conn)

st.sidebar.markdown("# :blue[DataCollab]")
menu()


if st.user.is_logged_in and "user" in st.session_state:
    st.subheader(f"👋 Hello :orange[{st.session_state['user']['name']}]")

    st.markdown("Here are some **recent projects** you might want to check out:")

    # Show last 5 added projects
    # recent_projects = utils.fetch_recent_projects(conn, limit=5)
    recent_projects = []

    if recent_projects:
        for project in recent_projects:
            st.markdown(f"""
                #### {project['title']}
                {project['description'][:120]}...
                🔧 Tech Stack: *{', '.join(project['tech_stack'])}*
                """)

            with st.expander("View Project"):
                st.markdown(f"[GitHub Repo]({project['github_url']})")
                st.markdown(f"🧑‍💻 Owner: {project['owner_name']} ({project['owner_email']})")
                st.markdown("---")
    else:
        st.info("No projects yet. Be the first to create one!")

    if st.button("Explore All Projects"):
        st.switch_page("pages/projects.py")

else:
    st.title(" 🧊 Welcome to DataCollab")
    st.subheader("🤝 Find. Collaborate. Grow.")

    st.markdown("""
    DataCollab is where developers discover and join open-source projects with ease.

    - 🔍 Find a project that matches your skills  
    - 🤝 Link up with a team and start building  
    - 🚀 Grow your portfolio through real collaboration
    """)

    st.write("")
    st.write("")

    if st.button("Explore Projects", icon=":material/browse:"):
        st.switch_page("pages/projects.py")

    if st.button("Login to Get Started", icon=":material/fingerprint:"):
        st.switch_page("pages/login.py")






