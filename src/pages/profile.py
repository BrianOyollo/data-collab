import streamlit as st

if st.user.is_logged_in:
    if st.session_state["user"]:
        user = st.session_state["user"]


        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="{user['profile_image']}" width="100" style="border-radius: 50%; margin-bottom: 10px;" />
                <h3 style="padding-bottom:1px;">{user['name']}</h3>
                <p>{user['email']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    
    st.json(st.user)

else:
    st.warning("You must login first to access this page")

