import streamlit as st
from sqlalchemy import text
from utils import utils
from menu import menu

conn = st.connection('sql')

st.header("Blogs")
st.sidebar.markdown("# :blue[DataCollab]")
utils.ensure_user_in_session(conn)
menu()

with conn.session as session:
    project_categories_results = session.execute(text("SELECT name FROM data_collab.categories")).fetchall()

categories = [row[0] for row in project_categories_results]
st.write(categories)

user_selection = st.multiselect("Project Category",placeholder="Pick a category that best matches the project", options=categories)
st.write(user_selection)