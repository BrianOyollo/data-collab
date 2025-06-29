INSERT INTO data_collab.tech_stack (name)
VALUES 
    ('Python'),
    ('SQL'),
    ('Apache Airflow'),
    ('Apache Spark'),
    ('Kafka'),
    ('dbt'),
    ('Pandas'),
    ('PostgreSQL'),
    ('MySQL'),
    ('MongoDB'),
    ('Snowflake'),
    ('BigQuery'),
    ('Redshift'),
    ('Delta Lake'),
    ('AWS S3'),
    ('AWS Glue'),
    ('Azure Data Factory'),
    ('Google Cloud Storage'),
    ('Docker'),
    ('Terraform'),
    ('scikit-learn'),
    ('TensorFlow'),
    ('PyTorch'),
    ('XGBoost'),
    ('LightGBM'),
    ('Keras'),
    ('Transformers'),
    ('spaCy'),
    ('Hugging Face'),
    ('MLflow'),
    ('Optuna'),
    ('NumPy'),
    ('Matplotlib'),
    ('Seaborn'),
    ('ONNX'),
    ('FastAI'),
    ('Excel'),
    ('Google Sheets'),
    ('Power BI'),
    ('Tableau'),
    ('Metabase'),
    ('Looker'),
    ('Jupyter Notebooks'),
    ('R'),
    ('Google Data Studio'),
    ('Pivot Tables'),
    ('Exploratory Data Analysis'),
    ('Statistics'),
    ('Dash'),
    ('Altair'),
    ('ggplot2'),
    ('D3.js'),
    ('Bokeh'),
    ('Chart.js'),
    ('Superset'),
    ('ECharts'),
    ('AWS'),
    ('GCP'),
    ('Azure'),
    ('Kubernetes'),
    ('Git'),
    ('GitHub Actions'),
    ('Prefect'),
    ('Airbyte'),
    ('Great Expectations'),
    ('Others')
ON CONFLICT (name) DO NOTHING;


INSERT INTO data_collab.roles (name)
VALUES 
    ('Data Engineer'),
    ('Machine Learning Engineer'),
    ('Data Scientist'),
    ('Data Analyst'),
    ('Business Intelligence Analyst'),
    ('Research Scientist'),
    ('AI Engineer'),
    ('MLOps Engineer'),
    ('Model Deployment Engineer'),
    ('Cloud Data Engineer'),
    ('Database Administrator'),
    ('ETL Developer'),
    ('Data Architect'),
    ('Data Platform Engineer'),
    ('Big Data Engineer'),
    ('Quantitative Analyst'),
    ('Data Visualization Specialist'),
    ('BI Developer'),
    ('Product Analyst'),
    ('Statistician'),
    ('Decision Scientist'),
    ('Analytics Engineer'),
    ('Deep Learning Engineer'),
    ('Computer Vision Engineer'),
    ('NLP Engineer'),
    ('AI Researcher'),
    ('Data Quality Analyst'),
    ('Data Governance Specialist'),
    ('Data Strategist'),
    ('DevOps Engineer (Data/ML Focus)')
ON CONFLICT (name) DO NOTHING;


INSERT INTO data_collab.categories (name)
VALUES 
    ('Data Engineering'),
    ('Data Science'),
    ('Machine Learning'),
    ('Deep Learning'),
    ('MLOps'),
    ('Artificial Intelligence'),
    ('Business Intelligence'),
    ('Data Analytics'),
    ('Data Visualization'),
    ('Natural Language Processing'),
    ('Computer Vision'),
    ('Big Data'),
    ('Cloud Computing'),
    ('DevOps for Data'),
    ('Data Governance'),
    ('Data Strategy'),
    ('Research & Development'),
    ('Open Data Projects'),
    ('Real-time Data Processing'),
    ('Predictive Analytics'),
    ('Recommender Systems'),
    ('Statistical Modeling'),
    ('Data Warehousing'),
    ('Dashboarding & Reporting')
ON CONFLICT (name) DO NOTHING;
