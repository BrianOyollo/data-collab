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
utils.ensure_user_in_session(conn)
menu()



# will run on st.rerun()
utils.display_messages()
