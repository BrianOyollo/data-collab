import streamlit as st
from utils import utils
import menu as menu
import time

st.set_page_config(
    page_title="Projects",
    page_icon="🧊",
    layout="wide",
)

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
    st.page_link("app.py", label="Home", icon=":material/home_app_logo:")
    menu.projects_menu()
    st.divider()

    # filters 

    filter_data = utils.filter_options(conn)


    filter_col, reset_col = st.columns(2)

    with filter_col:
        st.html("<h2 style='margin-top:0px; padding:0px'>Filters</h2>")
    
    with reset_col:
        # reset filters
        reset_filters = st.button("Reset", type="secondary", icon=":material/filter_list_off:", key="reset_filters", use_container_width=True)
        if reset_filters:
            st.session_state.collab_status_filter = None
            st.session_state.tech_stack_filter = []
            st.session_state.categories_filter = []
            st.session_state.roles_filter = []
            st.session_state.min_team_size = None
            st.session_state.max_team_size = None
            # st.rerun()

    # by collab status
    collab_filter = st.selectbox(
        "Collab status",
        options = ["Open to collabs", "Closed to collabs"],
        index=None,
        width="stretch",
        key="collab_status_filter"
    )

    # tech stack
    tech_stack_filter = st.multiselect(
        "Tech Stack",
        options = filter_data['tech_stach_filter_options'],
        key="tech_stack_filter"
    )

    # categories
    categories_filter = st.multiselect(
        "Project Categories",
        options = filter_data['categories_filter_options'],
        key="categories_filter"
    )

    # roles
    roles_filter = st.multiselect(
        "Desired Collaborations",
        options = filter_data['roles_filter_options'],
        key="roles_filter"
    )

    # team size
    st.write("Team Size")
    min_col, max_col = st.columns(2)
    with min_col:
        min_team_size = st.number_input(
            "Min", 
            min_value=0, 
            value = None,
            step=1, 
            label_visibility="collapsed", 
            placeholder="min",
            key="min_team_size"
        )

    with max_col:
        max_team_size = st.number_input(
            "Max", 
            min_value=0, 
            value=None, 
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