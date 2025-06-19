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


def create_project(conn):
    """
    Creates a new project with tech stack and desired roles.
    
    Args:
        conn: SQLAlchemy connection/session context
        project (dict): Dictionary containing project details and related fields
    """
    user = st.session_state["user"]
    project_data = {
        "title": st.session_state.get("new_project_project_title", "").strip(),
        "description": st.session_state.get("new_project_project_description", "").strip(),
        "project_categories":st.session_state.get("new_project_project_categories", []),
        "tech_stack": st.session_state.get("new_project_tech_stack", []),
        "collab_status": st.session_state.get("new_project_collab_status", ""),
        "desired_roles": st.session_state.get("new_project_desired_roles", []),
        "github_link": st.session_state.get("new_project_github_link", "").strip(),
        "owner": user["name"],
        "owner_email":user["email"]
    }
    if project_data["collab_status"] == "Maybe Later":
        project_data['desired_roles'] = None
    try:
        with conn.session as session:
            # insert into projects
            projects_query = text(
                """INSERT INTO data_collab.projects(title,description,github_url,is_open_to_collab,owner_name,owner_email)
                VALUES(:title, :description, :github_url, :is_open_to_collab, :owner_name, :owner_email)
                RETURNING id;
            """)
            result = session.execute(projects_query, {
                "title": project_data["title"],
                "description": project_data["description"],
                "github_url": project_data["github_link"],
                "is_open_to_collab": project_data["collab_status"] == "Yes",
                "owner_name": project_data["owner"],
                "owner_email": project_data["owner_email"],
            })
            project_id = result.scalar()

            # Insert into project_tech_stack (if any)
            if project_data["tech_stack"]:
                project_tech_stack_query = text("""
                    INSERT INTO data_collab.project_tech_stack(project_id, tech_stack_id)
                    SELECT :project_id, id FROM data_collab.tech_stack ts
                    WHERE ts.name = ANY(:selected_tech_stack)
                """)
                session.execute(project_tech_stack_query, {"project_id":project_id,"selected_tech_stack":project_data["tech_stack"]})

            # Insert into project_roles (if any)
            if project_data["desired_roles"]:
                project_roles_query = text("""
                    INSERT INTO data_collab.project_roles(project_id, role_id)
                    SELECT :project_id, id FROM data_collab.roles r
                    WHERE r.name = ANY(:desired_roles)
                """)
                session.execute(project_roles_query,{"project_id":project_id, "desired_roles":project_data['desired_roles']})

            # Insert into project_categories (if any)
            if project_data['project_categories']:
                project_categories_query = text("""
                    INSERT INTO data_collab.project_categories(project_id, category_id) 
                    SELECT :project_id, id FROM data_collab.categories c 
                    WHERE c.name = ANY(:project_categories)""")
                session.execute(project_categories_query,{"project_id":project_id, "project_categories":project_data["project_categories"]})

            # commit everything
            session.commit()
            st.success("🎉 Project created!")
            st.balloons()
    except Exception as e:
        raise