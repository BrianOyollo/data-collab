import streamlit as st
import menu as menu
from utils import utils

st.set_page_config(
    page_title="Projects",
    page_icon="🧊",
    layout="wide",
)

st.sidebar.markdown("# :blue[DataCollab]")
utils.display_messages()
menu.projects_menu()
menu.extras_menu()

if not st.user.is_logged_in:
    col1,col2,col3 = st.columns(3, vertical_alignment="center")

    with col2:
        st.header("Login", width="stretch")

        # google login
        if st.button("Login with Google", type="secondary", key="login_btn_google", use_container_width=True):
            st.login("google")

        # github login
        if st.button("Login with GitHub", type="secondary", key="login_btn_github", use_container_width=True):
            st.toast("GitHub login coming soon")

