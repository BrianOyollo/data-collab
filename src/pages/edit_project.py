import streamlit as st
from utils import utils
import menu as menu
import time


st.sidebar.markdown("# :blue[DataCollab]")
menu.menu()
st.subheader("Edit Project")

st.write(st.session_state["project"])