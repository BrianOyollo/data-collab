import streamlit as st
from sqlalchemy import text

def create_user(conn, user:dict):
    """
    Takes a logged in user and inserts into db if not already present
    Assumes user has name,email, picture (from google)
    """
    name = user['name']
    email = user['email']
    profile_image = user['picture']
    query = text("""
        INSERT INTO data_collab.users(name,email,profile_image)
        VALUES(%s,%s,%s)
        ON CONFLICT(email) DO NOTHING;
    """)
    with conn.session() as session:
        session.executr(query, (name,email,profile_image))
        session.commit()

def sync_user(conn, user:dict):
    """
    Ensures the logged in user exists in DB and stores user_id in session state.
    """
    email = user['email']
    if not email:
        return 
    
    with conn.session as session:
        result = session.execute(text("SELECT * FROM data_collab.users WHERE email =:email;"), {"email":email}).fetchone()
        if result:
            st.session_state['user'] = result._mapping
        else:
            session.execute(
                text("""INSERT INTO data_collab.users(name,email,profile_image) VALUES(:name,:email,:profile_image);"""), 
                {"name":user['name'],"email":user['email'], "profile_image":user['picture']}
            )
            session.commit()
            
            # fetch user data
            result = session.execute(text("SELECT * FROM data_collab.users WHERE email =:email;"), {"email":email}).fetchone()
            if result:
                st.session_state['user'] = result._mapping