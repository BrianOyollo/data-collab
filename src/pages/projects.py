import streamlit as st
from html import escape

from utils import utils

conn = st.connection("sql")

with st.spinner("Fetching projects...", show_time=True):
    project_results = utils.fetch_projects(conn)

if project_results is not None:
    projects = [row._mapping for row in project_results]
    st.subheader(f"Projects({len(projects)})")


    for project in projects:
        utils.project_fragement(conn,project)
        

else:
    st.subheader(f"Projects()")
    st.info("There are no projects to display right now")