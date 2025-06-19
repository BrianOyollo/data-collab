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





def add_bootstrap():
    bootstrap_str = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .project-card {
            transition: transform 0.2s;
            margin-bottom: 1.5rem;
        }
        .project-card:hover {
            transform: translateY(-2px);
        }
        .tech-badge {
            margin-right: 0.3rem;
            margin-bottom: 0.3rem;
            font-size: 0.7rem;
        }
        .role-badge {
            margin-right: 0.3rem;
            margin-bottom: 0.3rem;
        }
        .card-footer-item {
            font-size: 0.85rem;
        }
    </style>
    """
    return bootstrap_str

def project_card(project):
    with st.container(border=True):
    # Card header with title and description
        st.markdown(f"""
            <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="mb-1" style='color: #2c3e50;'>{project['title']}</h5>
                <span class="badge bg-{'success' if project['is_open_to_collab'] else 'secondary'}">
                    {'Open' if project['is_open_to_collab'] else 'Closed'} to Collab
                </span>
            </div>
            <p class="text-muted mb-3">{project['description']}</p>
            """, unsafe_allow_html=True)
            
            # Tech stack and roles in a row
        col1, col2 = st.columns(2)
            
        with col1:
            st.markdown("""
            <p class="fw-bold mb-1" style="color: #e67e22;">Tech Stack</p>
            <div class="d-flex flex-wrap">
            """ + 
            "".join([f'<span class="badge tech-badge bg-primary">{tech}</span>' for tech in project['tech_stack']]) +
            """
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <p class="fw-bold mb-1" style="color: #e67e22;">Desired Roles</p>
            <div class="d-flex flex-wrap">
            """ + 
            "".join([f'<span class="badge role-badge bg-info text-dark">{role}</span>' for role in project['desired_roles']]) +
            """
            </div>
            """, unsafe_allow_html=True)
            
            # Footer with metadata
            st.markdown("""
            <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top">
                <div>
                    <small class="fw-bold" style="color: #7f8c8d;">Owner</small><br>
                    <small>{owner}</small>
                </div>
                <div>
                    <small class="fw-bold" style="color: #7f8c8d;">Project URL</small><br>
                    <small><a href="{github_url}" target="_blank">GitHub Repository</a></small>
                </div>
                <div>
                    <small class="fw-bold" style="color: #7f8c8d;">Collaborators</small><br>
                    <small>{collab_count}</small>
                </div>
            </div>
            """.format(
                owner=project['owner'],
                github_url=project['github_url'],
                collab_count=len(project['collaborators'])
            ), unsafe_allow_html=True)
            
            # Join button if open to collaboration
        if project['is_open_to_collab']:
            st.markdown("""
            <div class="d-grid gap-2 mt-3">
                <button class="btn btn-success btn-sm" type="button">Join Project</button>
            </div>
            """, unsafe_allow_html=True)