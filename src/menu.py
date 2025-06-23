import streamlit as st
from utils import utils

conn = st.connection('sql')



# def ensure_user_in_session(conn):
#     if st.user.is_logged_in:
#         if "user" not in st.session_state:
#             utils.sync_user(conn, st.user)

def projects_menu():
    # st.sidebar.write(":orange[Projects]")
    st.sidebar.page_link("pages/projects.py", label="Projects", use_container_width=True)
    st.sidebar.page_link("pages/new_project.py", label="Add a Project", use_container_width=True)
    

def extras_menu():
    # st.sidebar.write(":orange[Extras]") 
    st.sidebar.page_link("pages/blogs.py", label="Blogs")
    st.sidebar.page_link("pages/about.py", label="About DataCollab")  


def authenticated_menu():
    st.sidebar.write(":orange[Account]")
    if "user" in st.session_state:
        st.sidebar.page_link("pages/profile.py", label="Your Profile")

        if st.sidebar.button("Logout", icon=":material/fingerprint_off:", key="logout_btn", use_container_width=True):
            st.logout()
    else:      
        st.sidebar.page_link("pages/login.py", label="Login", icon=":material/fingerprint:")
    
    


def admin_menu():
    st.sidebar.write(":orange[Admin]")



def menu():
    projects_menu()
    extras_menu()
    authenticated_menu()