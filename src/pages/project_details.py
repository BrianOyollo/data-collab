import streamlit as st
from utils import utils
from menu import menu


conn = st.connection("sql")
utils.ensure_user_in_session(conn)

st.sidebar.markdown("# :blue[DataCollab]")
menu()


st.header("Project Details")