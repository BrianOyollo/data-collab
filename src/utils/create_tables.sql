-- Create 'projects' table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    category TEXT,
    title TEXT NOT NULL,
    description TEXT,
    tech_stack TEXT, -- You can store JSON or comma-separated string
    github_url TEXT,
    is_open_to_collab BOOLEAN DEFAULT TRUE,
    desired_roles TEXT, -- Also can be JSON or comma-separated string
    owner_name TEXT,
    owner_email TEXT NOT NULL,
    time_created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    time_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create 'collaborators' table
CREATE TABLE IF NOT EXISTS collaborators (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_email TEXT NOT NULL,
    added_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_email)
);
