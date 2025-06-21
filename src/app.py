import streamlit as st
from utils import utils
from menu import menu
import time

conn = st.connection('sql')

st.set_page_config(
    page_title="DataCollab",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("# :blue[DataCollab]")

# will run on st.rerun()
if "ss_message" in st.session_state:
    message = st.session_state["ss_message"]
    if message is not None:
        st.toast(message["text"], icon=f'{message["icon"]}')
        time.sleep(4)
        del st.session_state["ss_message"]




if st.user.is_logged_in:
    if "user" not in st.session_state:
        utils.sync_user(conn, st.user)

menu()