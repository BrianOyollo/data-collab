
CREATE SCHEMA data_collab;

CREATE TABLE IF NOT EXISTS data_collab.users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE NOT NULL,
    profile_image TEXT,
    provider TEXT DEFAULT 'google', -- incase another provider is added
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- project categories
CREATE TABLE IF NOT EXISTS data_collab.categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- tech stack
CREATE TABLE IF NOT EXISTS data_collab.tech_stack (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- roles
CREATE TABLE IF NOT EXISTS data_collab.roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


--  project
CREATE TABLE IF NOT EXISTS data_collab.projects (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    github_url TEXT,
    is_open_to_collab BOOLEAN DEFAULT TRUE,
    owner_name TEXT,
    owner_email TEXT NOT NULL,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    time_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- project - tech stack
CREATE TABLE IF NOT EXISTS data_collab.project_tech_stack (
    project_id INTEGER REFERENCES data_collab.projects(id) ON DELETE CASCADE,
    tech_stack_id INTEGER REFERENCES data_collab.tech_stack(id) ON DELETE CASCADE,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, tech_stack_id)
);

-- project - desired collaborations(roles)
CREATE TABLE IF NOT EXISTS data_collab.project_roles (
    project_id INTEGER REFERENCES data_collab.projects(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES data_collab.roles(id) ON DELETE CASCADE,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, role_id)
);

-- project - project categories
CREATE TABLE IF NOT EXISTS data_collab.project_categories (
    project_id INTEGER NOT NULL REFERENCES data_collab.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES data_collab.categories(id) ON DELETE CASCADE,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, category_id)
);

-- project - collaborators
CREATE TABLE IF NOT EXISTS data_collab.project_collaborators (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES data_collab.projects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES data_collab.users(id) ON DELETE CASCADE,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);
