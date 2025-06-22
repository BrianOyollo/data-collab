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


# ============================================= SIDEBAR ============================================================
st.sidebar.markdown("# :blue[DataCollab]")
with st.sidebar:
    st.page_link("app.py", label="Back to main menu", icon=":material/arrow_left_alt:")
    menu.projects_menu()

    # filters 

    filter_data = utils.filter_options(conn)


    filter_col, reset_col = st.columns(2, vertical_alignment="top")
    
    with filter_col:
        st.subheader("Filters")
    
    with reset_col:
        reset_filters = st.button("Reset", type="tertiary", key="reset_filters")
        if reset_filters:
            st.session_state.collab_status_filter = None
            st.session_state.tech_stack_filter = []
            st.session_state.categories_filter = []
            st.session_state.roles_filter = []
            st.session_state.min_team_size = 0
            st.session_state.max_team_size = filter_data['max_team_size_filter']
            # st.rerun()

    # by collab status
    collab_filter = st.selectbox(
        ":orange[Collab status]",
        options = ["Open to collabs", "Closed to collabs"],
        index=None,
        width="stretch",
        key="collab_status_filter"
    )

    # tech stack
    tech_stack_filter = st.multiselect(
        ":orange[Tech Stack]",
        options = filter_data['tech_stach_filter_options'],
        key="tech_stack_filter"
    )

    # categories
    categories_filter = st.multiselect(
        ":orange[Project Categories]",
        options = filter_data['categories_filter_options'],
        key="categories_filter"
    )

    # roles
    roles_filter = st.multiselect(
        ":orange[Desired Collaborations]",
        options = filter_data['roles_filter_options'],
        key="roles_filter"
    )

    # team size
    st.write(":orange[Team Size]")
    min_col, max_col = st.columns(2)
    with min_col:
        min_team_size = st.number_input(
            "Min", 
            min_value=0, 
            step=1, 
            label_visibility="collapsed", 
            placeholder="min",
            key="min_team_size"
        )

    with max_col:
        max_team_size = st.number_input(
            "Max", 
            min_value=0, 
            value=filter_data['max_team_size_filter'], 
            step=1, 
            label_visibility="collapsed",
            placeholder="max", 
            key="max_team_size"
        )


filters = {
    "collab_status":collab_filter,
    "tech_stack": tech_stack_filter,
    "categories": categories_filter,
    "min_team_size": min_team_size,
    "max_team_size": max_team_size,
    "desired_collabs": roles_filter
}

# ============================================= END OF SIDEBAR ============================================================

# ============================================= MAIN SECTION ==============================================================
with st.spinner("Fetching projects...", show_time=True):
    project_results = utils.fetch_projects(conn, filters)

if project_results is not None:
    projects = [row._mapping for row in project_results]
    st.subheader(f"Projects({len(projects)})")


    for project in projects:
        utils.project_fragement(conn,project)
        

else:
    st.subheader(f"Projects()")
    st.info("There are no projects to display right now")

# ============================================= END OF MAIN SECTION ==============================================================