import streamlit as st

def projects_menu():
    # st.sidebar.write(":orange[Projects]")
    st.sidebar.page_link("pages/projects.py", label="Projects")
    st.sidebar.page_link("pages/new_project.py", label="Add a Project")

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