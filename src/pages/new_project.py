import streamlit as st

st.header("New Project")

if st.user.is_logged_in:
    st.success("you can create a project")
else:
    st.warning("You must login first to create a project")