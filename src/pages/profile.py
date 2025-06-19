import streamlit as st

if st.user.is_logged_in:
    st.image(st.user.picture)
    st.title(st.user.name)

    st.write(st.session_state['user'])

else:
    st.warning("You must login first to access this page")

