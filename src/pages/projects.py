import streamlit as st
from html import escape
from utils import utils




st.subheader(f"Projects(37)")





dummy_projects = [
    {
        "id":1,
        "category": "Data Visualization",
        "title": "Interactive Dashboard for Airbnb Listings with Artificial Intelligence",
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
        "owner": "John Doe",
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
        "owner": "Jane Doe",
        "collaborators": ["Aisha Noor", "Kelvin Otieno"]
    },
]


for project in dummy_projects:
   with st.container(border=True, key=f"cont_{project['id']}"):
        st.html(f"<h5 style='margin:0'>{project['title']}</h5>")
        st.html(f"<small>{project['description']}</small>")

        tech_stack, desired_roles = st.columns(2)
        tech_stack_items = " • ".join(project['tech_stack']) if isinstance(project['tech_stack'], list) else project['tech_stack']
        desired_roles_items = " | ".join(project['desired_roles']) if isinstance(project['desired_roles'], list) else project['desired_roles']

        with tech_stack:
            st.markdown(f"<small>:orange[Tech Stack]: </small></br> <small style='margin:0'>{tech_stack_items}</small>", unsafe_allow_html=True)

        with desired_roles:
            st.markdown(f"<small>:orange[Desired Roles:]</small> </br> <small style='margin:0'>{desired_roles_items}</small>", unsafe_allow_html=True)


        # projet github link
        project_link = f"[GitHub](project['github_url'])"

        # collab status
        collab_status = collab_status = "green-badge[:material/handshake: Open to Collab]"
        if not project['is_open_to_collab']:
            collab_status = "grey-badge[:material/handshake: Closed to Collab]"

        st.markdown(
            f"""
            :violet-badge[:material/deployed_code_account: {project['owner']}] 
            :blue-badge[:material/fork_right: {project_link}] 
            :{collab_status}
            :orange-badge[:material/groups: Current Members{len(project['collaborators'])}] 
            """

        )

        btn1,btn2,btn3 = st.columns(3)
        with btn2:
            if project['is_open_to_collab']:
                st.button("Join Project", type="tertiary", icon=":material/rocket_launch:", use_container_width=True, key=f"btn_{project['id']}")