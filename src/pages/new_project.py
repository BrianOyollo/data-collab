import streamlit as st

st.subheader("New Project")



def create_project_form():
    tech_stack = [
        "Python", "SQL", "Apache Airflow", "Apache Spark", "Kafka", "dbt",
        "Pandas", "PostgreSQL", "MySQL", "MongoDB", "Snowflake", "BigQuery",
        "Redshift", "Delta Lake", "AWS S3", "AWS Glue", "Azure Data Factory",
        "Google Cloud Storage", "Docker", "Terraform", "scikit-learn",
        "TensorFlow", "PyTorch", "XGBoost", "LightGBM", "Keras", "Transformers",
        "spaCy", "Hugging Face", "MLflow", "Optuna", "NumPy", "Matplotlib",
        "Seaborn", "ONNX", "FastAI", "Excel", "Google Sheets", "Power BI",
        "Tableau", "Metabase", "Looker", "Jupyter Notebooks", "R",
        "Google Data Studio", "Pivot Tables", "Exploratory Data Analysis",
        "Statistics", "Dash", "Altair", "ggplot2", "D3.js", "Bokeh", "Chart.js",
        "Superset", "ECharts", "AWS", "GCP", "Azure", "Kubernetes", "Git",
        "GitHub Actions", "Prefect", "Airbyte", "Great Expectations", "Others"
    ]
    roles = [
        "Data Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Data Analyst",
        "Business Intelligence Analyst",
        "Research Scientist",
        "AI Engineer",
        "MLOps Engineer",
        "Model Deployment Engineer",
        "Cloud Data Engineer",
        "Database Administrator",
        "ETL Developer",
        "Data Architect",
        "Data Platform Engineer",
        "Big Data Engineer",
        "Quantitative Analyst",
        "Data Visualization Specialist",
        "BI Developer",
        "Product Analyst",
        "Statistician",
        "Decision Scientist",
        "Analytics Engineer",
        "Deep Learning Engineer",
        "Computer Vision Engineer",
        "NLP Engineer",
        "AI Researcher",
        "Data Quality Analyst",
        "Data Governance Specialist",
        "Data Strategist",
        "DevOps Engineer (Data/ML Focus)"
    ]

    with st.form("New Project"):
        title = st.text_input("Title:", key="new_project_project_title")
        description = st.text_area("Description", key="new_project_project_description")
        
        with st.expander("Tech Stack"):
            st.pills("The project will use...", options=tech_stack,selection_mode="multi", key="new_project_tech_stack")
        
        collab_status = st.radio(
            "Are you open to collaborations?",
            options=["Yes", "Maybe Later"],
            captions=["", "Selected collaborations below won't be saved"],
            horizontal=True,
            key="new_project_collab_status"
        )
        with st.expander("Collaborations"):
            desired_roles = st.pills("Looking to collaborate with...", options=roles,selection_mode="multi", key="new_project_desired_roles")

        github_url = st.text_input("GitHub link", key="new_project_github_link")
        create_project = st.form_submit_button("Create")
        return create_project

if st.user.is_logged_in:
    create_project = create_project_form()
    if create_project:
        new_project_data = {
            "title": st.session_state.get("new_project_project_title", "").strip(),
            "description": st.session_state.get("new_project_project_description", "").strip(),
            "tech_stack": st.session_state.get("new_project_tech_stack", []),
            "collab_status": st.session_state.get("new_project_collab_status", ""),
            "desired_roles": st.session_state.get("new_project_desired_roles", []),
            "github_link": st.session_state.get("new_project_github_link", "").strip(),
            "owner": st.user.email  # or st.user.name or any identifier for the logged-in user
        }
        if st.session_state.get("new_project_collab_status") == "Maybe Later":
            new_project_data['desired_roles'] = None

        st.success("🎉 Project created!")
        st.json(new_project_data)

else:
    st.warning("You must login first to create a project")