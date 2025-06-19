import streamlit as st

if st.user.is_logged_in:
    if st.session_state["user"]:
        user = st.session_state["user"]

        col1,col2,col3 = st.columns(3)
        with col2:
            st.image(user["profile_image"], width=100, use_container_width=False)
            st.subheader(user["name"], width="stretch")
            st.write(user["email"])

    
    st.json(st.user)

else:
    st.warning("You must login first to access this page")

