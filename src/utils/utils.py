import streamlit as st
from sqlalchemy import text,exc


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
        "owner_email":user["email"],
        "owner_id":user["id"]
    }
    if project_data["collab_status"] == "Maybe Later":
        project_data['desired_roles'] = None
    try:
        with conn.session as session:
            # insert into projects
            projects_query = text(
                """INSERT INTO data_collab.projects(title,description,github_url,is_open_to_collab,owner_id)
                VALUES(:title, :description, :github_url, :is_open_to_collab, :owner_id)
                RETURNING id;
            """)
            result = session.execute(projects_query, {
                "title": project_data["title"],
                "description": project_data["description"],
                "github_url": project_data["github_link"],
                "is_open_to_collab": project_data["collab_status"] == "Yes",
                "owner_id": project_data["owner_id"],
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


def fetch_projects(conn):
    query = text("""
        SELECT
            p.id, p.title,p.description,p.github_url,p.is_open_to_collab, p.time_created,p.time_updated,
            u.name AS owner,
            u.email,
            ARRAY_AGG(DISTINCT c.name) AS categories,
            ARRAY_AGG(DISTINCT ts.name) AS tech_stack,
            ARRAY_AGG(DISTINCT r.name) AS desired_roles,
            COUNT(DISTINCT collab.user_id) AS collaborators
        FROM data_collab.projects p
        LEFT JOIN data_collab.project_categories pc ON pc.project_id=p.id
        LEFT JOIN data_collab.project_tech_stack pts ON pts.project_id=p.id
        LEFT JOIN data_collab.project_roles pr ON pr.project_id=p.id
        LEFT JOIN data_collab.project_collaborators collab ON collab.project_id=p.id
        LEFT JOIN data_collab.users u ON p.owner_id=u.id
        LEFT JOIN data_collab.categories c ON c.id=pc.category_id
        LEFT JOIN data_collab.tech_stack ts ON ts.id=pts.tech_stack_id
        LEFT JOIN data_collab.roles r ON r.id=pr.role_id
        GROUP BY p.id, u.name,u.email
        ORDER BY p.time_created DESC;
    """)
    with conn.session as session:
        results = session.execute(query).fetchall()

    return results

def is_user_collaborator(conn, project_id:int, user_id:int)->bool:
    # check is user is a project collaborator
    # returns True or False

    with conn.session as session:
        result = session.execute(
            text("""SELECT 1 FROM data_collab.project_collaborators WHERE project_id=:project_id AND user_id=:user_id;"""),
            {"project_id":project_id, "user_id":user_id}
        ).fetchone()
    return result is not None

def join_project(conn, project_id:int):
    """
    Add user as collaborator

    Args:
        conn: SQLAlchemy connection/session context
        project_id (int): project id
        user_id (int): user id
    """
    if not "user" in st.session_state:
        st.toast(":red[You must login to join a project]", icon=":material/block:")
        return
    
    user_id = st.session_state["user"]["id"]
    try:
        with conn.session as session:
            session.execute(text(
                """INSERT INTO data_collab.project_collaborators(project_id,user_id)
                VALUES(:project_id, :user_id)"""), {"project_id":project_id, "user_id":user_id}
            )
            session.commit()
            st.toast(":green[Done! Happy coding!]", icon=":material/celebration:")
    except exc.IntegrityError:
        st.toast("Aready part of the project")
    except Exception as e:
        st.toast("Looks like there's problem. Please try again later or contact your system admin")
