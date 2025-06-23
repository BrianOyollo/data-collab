import streamlit as st
from sqlalchemy import text,exc
import time

def ensure_user_in_session(conn):
    # ensures the logged in user is always in session
    if st.user.is_logged_in:
        if "user" not in st.session_state:
            sync_user(conn, st.user)

def display_messages():
    if "ss_message" in st.session_state:
        message = st.session_state["ss_message"]
        if message is not None:
            st.toast(message["text"], icon=f'{message["icon"]}')
            # time.sleep(4)
            del st.session_state["ss_message"]

def add_session_state_msg(msg:dict):
    # adds messages to session state
    # used to go around st.reruns()
    st.session_state["ss_message"] = msg

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
    
    try:
        with conn.session as session:
            result = session.execute(
                text("""
                    SELECT 
                        id,
                        name,
                        email,
                        profile_image,
                        DATE(time_created) AS joining_date,
                        phone,github_url,linkedin_url,portfolio_url
                    FROM data_collab.users WHERE email =:email;
                """),
                {"email":email}
            ).fetchone()
            if result:
                st.session_state['user'] = dict(result._mapping)
            else:
                session.execute(
                    text("""INSERT INTO data_collab.users(name,email,profile_image) VALUES(:name,:email,:profile_image);"""), 
                    {"name":user['name'],"email":user['email'], "profile_image":user['picture']}
                )
                session.commit()
                
                # fetch user data
                result = session.execute(
                    text("""
                        SELECT 
                            id,
                            name,
                            email,
                            profile_image,
                            DATE(time_created) AS joining_date,
                            phone,github_url,linkedin_url,portfolio_url
                        FROM data_collab.users WHERE email =:email;
                    """),
                    {"email":email}
                ).fetchone()
                if result:
                    st.session_state['user'] = dict(result._mapping)
        # st.toast(":violet[User synced to db]", icon=":material/check:")
    except Exception as e:
        st.toast("Error syncing user to db", icon=":material/error")


@st.fragment
def project_fragement(conn, project):
    with st.container(border=True, key=f"cont_{project['id']}"):
        # st.html(f"<h4 style='margin:0'>{project['title']}</h4>")
        # st.subheader(project['title'])
        st.page_link("pages/project_details.py", label=f"{project['title']}", use_container_width=True)
        st.html(f"<p style='white-space:pre-wrap; color='gray'>{project['description']}</p>")

        tech_stack_items = " / ".join(str(item) for item in project.get('tech_stack') or [] if item)
        desired_roles_items = " / ".join(str(item) for item in project.get("desired_roles") or [] if item)
        categories = " / ".join(str(item) for item in project.get('categories') or [] if item)

        tech_stack, desired_roles, project_category = st.tabs(["Tech Stack","Looking to collab with","Project Categories"])
        with tech_stack:
            st.markdown(f"<span style='margin:0'>{tech_stack_items}</span>", unsafe_allow_html=True)

        with desired_roles:
            st.markdown(f"<span style='margin:0'>{desired_roles_items}</span>", unsafe_allow_html=True)

        with project_category:
            st.markdown(f"<span style='margin:0'>{categories}</span>", unsafe_allow_html=True)


        # projet github link
        project_link = f"[GitHub]({project['github_url']})"

        # collab status
        collab_status = collab_status = "green-badge[:material/handshake: Open to Collab]"
        if not project['is_open_to_collab']:
            collab_status = "grey-badge[:material/handshake: Closed to Collab]"

        st.markdown(
            f"""
            :violet-badge[:material/deployed_code_account: {project['owner_name']}] 
            :blue-badge[:material/fork_right: {project_link}] 
            :{collab_status}
            :orange-badge[:material/groups: Current Members: {project['collaborators']}] 
            """

        )


        st.write("")
        btn1,btn2,btn3 = st.columns(3)

        # if user is logged in
        if "user" in st.session_state:

            # if user is a project collaborator
            # show leave button
            # otherwise join project button if project alllows collaborations
            if is_user_collaborator(conn, project['id'], st.session_state["user"]["id"]):
                with btn2:
                    leave_project_btn = st.button(
                        "Leave Project",
                        type="tertiary", 
                        icon=":material/door_open:", 
                        use_container_width=True
                        ,key=f"leave_project_btn_{project['id']}"
                    )
                    if leave_project_btn:
                        leave_project(conn,project["id"])
                        
            else:
                with btn2:
                    if project['is_open_to_collab']:
                        join_project_btn = st.button(
                            "Join Project", 
                            type="tertiary", 
                            icon=":material/rocket_launch:", 
                            use_container_width=True, 
                            key=f"join_project_btn_{project['id']}"
                        )
                        if join_project_btn:
                            project_id = project['id']
                            join_project(conn, project_id)
                            

            # if user logged in user is project owner
            # show delete project button 
            if project["owner_email"] == st.session_state["user"]["email"]: 
                with btn1:
                    edit_project_btn = st.button(
                        "Edit Project",
                        type="tertiary",
                        icon=":material/edit_square:",
                        use_container_width=True,
                        key=f"edit_project_btn_{project["id"]}"
                    )
                    if edit_project_btn:
                        st.session_state["original_project"] = project
                        edit_project(conn)
                        

                with btn3:  
                    delete_project_btn = st.button(
                        "Delete Project",
                        type="tertiary", 
                        icon=":material/delete:", 
                        use_container_width=True, 
                        key=f"dlt_project_btn_{project['id']}"
                    )
                    if delete_project_btn:
                        delete_project(conn, project["id"])
                        
                        

        # user is not logged in
        # show join project if project is open to collaborations
        else:
            if project['is_open_to_collab']:
                with btn2:
                    join_project_btn = st.button(
                        "Join Project", 
                        type="tertiary", 
                        icon=":material/rocket_launch:", 
                        use_container_width=True, 
                        key=f"btn_{project['id']}"
                    )
                    if join_project_btn:
                        project_id = project['id']
                        join_project(conn, project_id)



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
                    WHERE r.name = ANY(:desired_roles);
                """)
                session.execute(project_roles_query,{"project_id":project_id, "desired_roles":project_data['desired_roles']})

            # Insert into project_categories (if any)
            if project_data['project_categories']:
                project_categories_query = text("""
                    INSERT INTO data_collab.project_categories(project_id, category_id) 
                    SELECT :project_id, id FROM data_collab.categories c 
                    WHERE c.name = ANY(:project_categories);""")
                session.execute(project_categories_query,{"project_id":project_id, "project_categories":project_data["project_categories"]})

            # insert into project_collaborators
            project_collaborators_query = text("""
                INSERT INTO data_collab.project_collaborators(project_id, user_id)
                VALUES(:project_id,:user_id);""")
            session.execute(project_collaborators_query, {"project_id":project_id, "user_id":project_data["owner_id"]})
            
            # commit everything
            session.commit()
            st.success("🎉 Project created!")
            st.balloons()
    except Exception as e:
        st.toast(":red[Error creating project. Please try again later or contact the system admin]", icon="material/error:" )
        raise


def fetch_projects(conn, filters:dict):

    # takes dict of filters
    # contructs one sql query
    # filters = {
    #     "collab_status":collab_filter,
    #     "tech_stack": tech_stach_filter,
    #     "categories": categories_filter,
    #     "team_size": team_size_filter,
    #     "desired_collabs": roles_filter
    # }

    where_clause = []
    having_clause = []
    query_params = {}

    # collab status
    if filters['collab_status']:
        where_clause.append("pb.is_open_to_collab = :collab_status")
        query_params['collab_status'] = filters['collab_status'] == "Open to collabs" # will return True/False to match db

    # tech stack
    if filters['tech_stack']:
        where_clause.append("pb.tech_stack && :tech_stack")
        query_params['tech_stack'] = filters['tech_stack']

    # categories
    if filters['categories']:
        where_clause.append("pb.categories && :categories")
        query_params['categories'] = filters['categories']

    # desired collabs
    if filters['desired_collabs']:
        where_clause.append("pb.desired_roles && :desired_collabs")
        query_params['desired_collabs'] = filters['desired_collabs']

    # team size
    if filters['min_team_size'] is not None and filters['max_team_size'] is not None:
        where_clause.append("pb.collaborators BETWEEN :min_team_size AND :max_team_size")
        query_params["min_team_size"] = filters['min_team_size']
        query_params["max_team_size"] = filters['max_team_size']

    elif filters['min_team_size'] is not None:
        where_clause.append("pb.collaborators >= :min_team_size")
        query_params["min_team_size"] = filters['min_team_size']

    elif filters['max_team_size'] is not None:
        where_clause.append("pb.collaborators <= :max_team_size")
        query_params["max_team_size"] = filters['max_team_size']


    # combine clauses
    combined_where_clause = f"WHERE {' AND '.join(where_clause)}" if where_clause else ""
    # combined_having_clause = f"HAVING {'AND '.join(having_clause)}" if having_clause else ""

    query = text(f"""
        WITH projects_base AS(
            SELECT
                p.id, 
                p.title,
                p.description,
                p.github_url,
                p.is_open_to_collab, 
                p.time_created,
                p.time_updated,
                u.name AS owner_name,
                u.email AS owner_email,
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
            ORDER BY p.time_created DESC
        )
        SELECT * FROM projects_base pb
        {combined_where_clause}
        ;
    """)

    try:
        with conn.session as session:
            results = session.execute(query, query_params).fetchall()
        return results
    except Exception as e:
        # log e
        st.toast(":red[Error fetching projects. Please reload the page or contact the system admin]",icon=":material/error:" )
        raise

def is_user_collaborator(conn, project_id:int, user_id:int)->bool:
    # check is user is a project collaborator
    # returns True or False

    try:
        with conn.session as session:
            result = session.execute(
                text("""SELECT 1 FROM data_collab.project_collaborators WHERE project_id=:project_id AND user_id=:user_id;"""),
                {"project_id":project_id, "user_id":user_id}
            ).fetchone()
        return result is not None
    except Exception as e:
        # log the error
        return False

def join_project(conn, project_id:int):
    """
    Adds logged in user as prroject collaborator

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
            st.rerun(scope="fragment")

    except exc.IntegrityError:
        st.toast("Aready part of the project")
    except Exception as e:
        st.toast("Looks like there's problem. Please try again later or contact your system admin")



def leave_project(conn, project_id:int)->True:
    ## removes logged in user as a project collaborator

    if "user" not in st.session_state:
        return
    
    user = st.session_state["user"]

    try:
        with conn.session as session:
            result = session.execute(
                text("DELETE FROM data_collab.project_collaborators WHERE project_id=:project_id AND user_id=:user_id;"),
                {"project_id":project_id, "user_id":user["id"]}
            )
            session.commit()
            st.toast("Request successful", icon=":material/check_small:")
            st.rerun(scope="fragment")

    except Exception:
        st.toast(":red[Error compeleting request. Please try again later or contact the system admin]", icon=":material/error:")
        raise

@st.dialog("Delete Project")
def delete_project(conn, project_id:int)->True:
    ## deletes project if logged in user is the project owner

    if "user" not in st.session_state:
        return
    
    st.write(":red[Are you sure you want to delete this project? There might be active collaborators]")
    st.write("If you aren't sure, please hit cancel")

    user = st.session_state["user"]

    if st.button("Delete Project"):
        try:
            with conn.session as session:
                session.execute(
                    text("DELETE FROM data_collab.projects WHERE id=:project_id AND owner_id=:user_id;"),
                    {"project_id":project_id, "user_id":user["id"]}
                )
                session.commit()
                message = {"text":"Well, it was fun while it lasted. Create a new one soon", "icon":":material/check_small:"}
                add_session_state_msg(message)
                st.switch_page("pages/projects.py")
                

        except Exception:
            st.toast(":red[Error compeleting request. Please try again later or contact the system admin]", icon=":material/error:")
            raise


def update_project(conn):

    # user must be logged in
    if not st.user.is_logged_in:
        st.switch_page("pages/login.py")

    user = st.session_state["user"]

    # current project details
    project = st.session_state['original_project']

    if user["email"] != project["owner_email"]:
        st.toast(":red[You are not allowed not edit this project]", icon=":material/error:")
        return


    updated_project_data = {
        "title": st.session_state.get("edit_project_project_title", "").strip(),
        "description": st.session_state.get("edit_project_project_description", "").strip(),
        "project_categories":st.session_state.get("edit_project_project_categories", []),
        "tech_stack": st.session_state.get("edit_project_tech_stack", []),
        "collab_status": st.session_state.get("edit_project_collab_status", "") == "Yes",
        "desired_roles": st.session_state.get("edit_project_desired_roles", []),
        "github_link": st.session_state.get("edit_project_github_link", "").strip(),
        "owner": user["name"],
        "owner_email":user["email"],
        "owner_id":user["id"]
    }
    if updated_project_data["collab_status"] == "Maybe Later":
        updated_project_data['desired_roles'] = None

    try:
        with conn.session as session:
            project_update_query = text("""
                UPDATE data_collab.projects
                SET title=:title,description=:description,github_url=:github_url,is_open_to_collab=:collab_status
                WHERE id=:project_id AND owner_id=:owner_id
                RETURNING id;"""
            )

            # update projects table
            session.execute(project_update_query,{
                "title":updated_project_data["title"],
                "description":updated_project_data["description"],
                "github_url":updated_project_data["github_link"],
                "collab_status":updated_project_data["collab_status"],
                "project_id":project["id"],
                "owner_id":updated_project_data["owner_id"]

            })

            # clear tech stack, categories and desired roles mappings
            session.execute(
                text("DELETE FROM data_collab.project_tech_stack WHERE project_id = :project_id"),
                {"project_id": project["id"]}
            )
            session.execute(
                text("DELETE FROM data_collab.project_roles WHERE project_id = :project_id"),
                {"project_id": project["id"]}
            )
            session.execute(
                text("DELETE FROM data_collab.project_categories WHERE project_id = :project_id"),
                {"project_id": project["id"]}
            )

            # update tech stack
            if updated_project_data['tech_stack']:
                updated_tech_stack_query = text("""INSERT INTO data_collab.project_tech_stack(project_id,tech_stack_id)
                    SELECT :project_id, id FROM data_collab.tech_stack ts
                    WHERE ts.name=ANY(:tech_stack);""")
                session.execute(updated_tech_stack_query, {
                    "project_id":project['id'], "tech_stack":updated_project_data['tech_stack']
                })
        
            # update categories
            if updated_project_data["project_categories"]:
                update_categories_query = text("""
                    INSERT INTO data_collab.project_categories(project_id, category_id)
                    SELECT :project_id, id FROM data_collab.categories c
                    WHERE c.name = ANY(:categories)
                """)
                session.execute(update_categories_query, {
                    "project_id": project["id"],
                    "categories": updated_project_data["project_categories"]
                })
            
            # update roles
            if updated_project_data['desired_roles']:
                if updated_project_data["desired_roles"]:
                    update_roles_query = text("""
                        INSERT INTO data_collab.project_roles(project_id, role_id)
                        SELECT :project_id, id FROM data_collab.roles r
                        WHERE r.name = ANY(:roles)
                    """)
                    session.execute(update_roles_query, {
                        "project_id": project["id"],
                        "roles": updated_project_data["desired_roles"]
                    })

            session.commit()
            st.toast(":green[Project successfully updated]", icon=":material/celebration:")
            st.rerun()
    except Exception:
        st.toast(":red[Error updating project. Please try again later or contact your system admin]", icon=":material/error:")
        raise

@st.dialog("Edit Project", width="large")
def edit_project(conn):

    # current project details
    project = st.session_state['original_project']

    project_categories = []
    tech_stacks = []
    roles = []
    with conn.session as session:
        # tech stacks
        project_categories_results = session.execute(text("SELECT name FROM data_collab.categories")).fetchall()
        project_categories = [row[0] for row in project_categories_results]

        # tech stacks
        tech_stack_results = session.execute(text("SELECT name FROM data_collab.tech_stack")).fetchall()
        tech_stacks = [row[0] for row in tech_stack_results]

        # desired collaborations
        roles_results = session.execute(text("SELECT name FROM data_collab.roles")).fetchall()
        roles = [row[0] for row in roles_results]


    
    with st.form("Edit Project"):
        title = st.text_input("Title:", value=project['title'], key="edit_project_project_title")
        description = st.text_area("Description", value=project['description'], key="edit_project_project_description")

        project_categories = st.multiselect(
            "Project Category(s)", 
            options=project_categories,
            default=project['categories'],
            placeholder="AI, data engineering, frontend development,...", 
            key="edit_project_project_categories"
        )

        tech_stack = st.multiselect(
            "Tech Stack", 
            options=tech_stacks,
            default=project['tech_stack'],
            placeholder="python, sql, excel,...", key="edit_project_tech_stack")
        
        collab_status = st.radio(
            "Are you open to collaborations?",
            options=["Yes", "Maybe Later"],
            captions=["", "Selected collaborations below won't be saved"],
            horizontal=True,
            key="edit_project_collab_status"
        )

        desired_roles = st.multiselect(
            "Collaborations", 
            options=roles, 
            default = project['desired_roles'],
            placeholder="pick the roles you want to collaborate with", 
            key="edit_project_desired_roles"
        )

        github_url = st.text_input("GitHub link",
            value=project['github_url'], 
            placeholder="https://github.com/janedoe",
            label_visibility="visible",
            help="Please enter a full GitHub url",
            key="edit_project_github_link")

        st.write(" ")
        edit_project = st.form_submit_button(
            ":orange[Save Changes]", 
            type="tertiary", 
            use_container_width=True,
            icon=":material/save:")


        if edit_project:
            update_project(conn)
            # st.toast(st.user)



    
def filter_options(conn):
    # fetches data from db to populate filters
    tech_stach_filter_options = []
    categories_filter_options = []
    roles_filter_options = []
    max_team_size_filter = 1

    with conn.session as session:
        
        # tech stack
        ts_results = session.execute(text("SELECT DISTINCT name FROM data_collab.tech_stack;"))
        tech_stach_filter_options = [row[0] for row in ts_results.fetchall()]

        # categories
        cats_results = session.execute(text("SELECT DISTINCT name FROM data_collab.categories;"))
        categories_filter_options = [row[0] for row in cats_results.fetchall()]

        # desired collaborations
        roles_results = session.execute(text("SELECT DISTINCT name FROM data_collab.roles;"))
        roles_filter_options = [row[0] for row in roles_results.fetchall()]

        # team size
        max_team_size = session.execute(
            text("""
                SELECT MAX(member_count) 
                FROM (
                    SELECT COUNT(*) as member_count
                    FROM data_collab.project_collaborators
                    GROUP BY project_id
                ) as grouped;
            """)).scalar()

        max_team_size_filter = max_team_size

    return {
        "tech_stach_filter_options":tech_stach_filter_options,
        "categories_filter_options":categories_filter_options,
        "roles_filter_options":roles_filter_options,
        "max_team_size_filter":max_team_size_filter
    }