import streamlit as st
from html import escape
from utils import utils

st.header("Projects")

dummy_projects = [
    {
        "id":1,
        "category": "Data Visualization",
        "title": "Interactive Dashboard for Airbnb Listings",
        "description": "We are building an interactive dashboard to visualize Airbnb listings by city, room type, and price range using the anonymized OpenDataSoft dataset. The dashboard will allow filtering by various parameters and map-based visualizations with Leaflet or Mapbox.",
        "tech_stack": ["JavaScript", "React", "D3.js", "Mapbox", "Flask"],
        "github_url": "https://github.com/boyollo/airbnb-dashboard",
        "is_open_to_collab": True,
        "desired_roles": ["Frontend Developer", "Data Visualization Specialist", "UX Designer"],
        "owner": "Brian Oyollo",
        "collaborators": ["John Ouma", "Fatima Elmi"]
    },
    {
        "id":2,
        "category": "Artificial Intelligence",
        "title": "AI Resume-to-Job Matching System",
        "description": "This project builds an AI system that takes resumes and job descriptions and predicts the best matches based on skill overlap, experience, and role requirements. It uses NLP techniques and vector similarity to rank candidate-job pairs.",
        "tech_stack": ["Python", "spaCy", "HuggingFace Transformers", "FastAPI", "PostgreSQL"],
        "github_url": "https://github.com/boyollo/ai-resume-matcher",
        "is_open_to_collab": True,
        "desired_roles": ["NLP Engineer", "Backend Developer", "HR Tech Enthusiast"],
        "owner": "Brian Oyollo",
        "collaborators": ["Aisha Noor", "Kelvin Otieno"]
    },
    {
        "id":3,
        "category": "Climate Tech",
        "title": "Global Climate Trends Dashboard",
        "description": "An open-source dashboard visualizing temperature anomalies, CO₂ levels, and climate events globally using public datasets from NASA and NOAA. The goal is to build public awareness around climate change through compelling, interactive visuals.",
        "tech_stack": ["Python", "Dash", "Plotly", "GeoPandas", "Docker"],
        "github_url": "https://github.com/boyollo/climate-trends-dashboard",
        "is_open_to_collab": False,
        "desired_roles": ["Data Scientist", "Frontend Developer", "Environmental Analyst"],
        "owner": "Brian Oyollo",
        "collaborators": ["Chloe Mwangi", "Victor Ndeti"]
    },
    {
        "id":4,
        "category": "Data Visualization",
        "title": "Interactive Dashboard for Airbnb Listings",
        "description": "We are building an interactive dashboard to visualize Airbnb listings by city, room type, and price range using the anonymized OpenDataSoft dataset. The dashboard will allow filtering by various parameters and map-based visualizations with Leaflet or Mapbox.",
        "tech_stack": ["JavaScript", "React", "D3.js", "Mapbox", "Flask"],
        "github_url": "https://github.com/boyollo/airbnb-dashboard",
        "is_open_to_collab": True,
        "desired_roles": ["Frontend Developer", "Data Visualization Specialist", "UX Designer"],
        "owner": "Brian Oyollo",
        "collaborators": ["John Ouma", "Fatima Elmi"]
    },
    {
        "id":5,
        "category": "Artificial Intelligence",
        "title": "AI Resume-to-Job Matching System",
        "description": "This project builds an AI system that takes resumes and job descriptions and predicts the best matches based on skill overlap, experience, and role requirements. It uses NLP techniques and vector similarity to rank candidate-job pairs.",
        "tech_stack": ["Python", "spaCy", "HuggingFace Transformers", "FastAPI", "PostgreSQL"],
        "github_url": "https://github.com/boyollo/ai-resume-matcher",
        "is_open_to_collab": True,
        "desired_roles": ["NLP Engineer", "Backend Developer", "HR Tech Enthusiast"],
        "owner": "Brian Oyollo",
        "collaborators": ["Aisha Noor", "Kelvin Otieno"]
    },
]

# for i in range(0, len(dummy_projects), 3):
#     cols = st.columns(3, border=True)  # Make 3 side-by-side columns
#     for j in range(3):  # Fill each column
#         if i + j < len(dummy_projects):  # Check bounds
#             with cols[j]:  # Add item to that column
#                 project = dummy_projects[i + j]
#                 utils.generate_project_card(project)
#                 # join project card
#                 col1, col2, col3 = st.columns([1, 2, 1])
#                 with col2:
#                     if st.button("🚀 Join This Project", key=f"project_{project['id']}"):
#                         st.success("You've requested to join this project!")

with st.container():
    project = dummy_projects[0]
    tech_stack = " • ".join(project['tech_stack']) if isinstance(project['tech_stack'], list) else project['tech_stack']
    desired_roles = " | ".join(project['desired_roles']) if isinstance(project['desired_roles'], list) else project['desired_roles']
    collaborators = ", ".join(project['collaborators']) if isinstance(project['collaborators'], list) else project['collaborators']

    st.markdown(f"""
    <h2 style="color:#333;">{project['title']}</h2>

    <p><strong>Description:</strong><br>{project['description']}</p>

    <p><strong>Tech Stack:</strong> {tech_stack}</p>

    <p><strong>Desired Roles:</strong> {desired_roles}</p>

    <p><strong>Open to Collaboration:</strong> {"✅ Yes" if project['is_open_to_collab'] else "❌ No"}</p>

    <p><strong>Collaborators:</strong> {collaborators}</p>

    <p>
        🔗 <a href="{project['github_url']}" target="_blank" style="color: #4f46e5; font-weight: bold;">GitHub Repository</a>
    </p>
    """, unsafe_allow_html=True)

    # Center the Join Project button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Join This Project"):
            st.success("You've requested to join this project!")




