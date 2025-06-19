import streamlit as st


def generate_project_card(project:dict)->str:
    tech_stack = " • ".join(project['tech_stack']) if isinstance(project['tech_stack'], list) else project['tech_stack']
    desired_roles = " | ".join(project['desired_roles']) if isinstance(project['desired_roles'], list) else project['desired_roles']
    collaborators = ", ".join(project['collaborators']) if isinstance(project['collaborators'], list) else project['collaborators']

    card = st.markdown(f"""
        <div style="
            background-color: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 1.2rem;
            border: 1px solid #e0e0e0;
            font-size: 15px;
        ">
            <h4 style="color: #333; margin-bottom: 0.4rem;">{project['title']}</h4>
            <p style="color: #555; margin: 0.2rem 0;"><strong>Description:</strong> {project['description']}</p>
            <p style="color: #555; margin: 0.2rem 0;"><strong>Tech Stack:</strong> {tech_stack}</p>
            <p style="color: #555; margin: 0.2rem 0;"><strong>Desired Roles:</strong> {desired_roles}</p>
            <p style="color: #555; margin: 0.2rem 0;"><strong>Open to Collaboration:</strong> {"✅ Yes" if project['is_open_to_collab'] else "❌ No"}</p>
            <p style="color: #555; margin: 0.2rem 0;"><strong>Collaborators:</strong> {collaborators}</p>
            <p style="margin-top: 0.4rem;">
                🔗 <a href="{project['github_url']}" target="_blank" style="color: #4f46e5; font-weight: bold;">GitHub Repository</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

    return card
