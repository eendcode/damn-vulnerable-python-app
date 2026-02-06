-- 1. Create the primary users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL,
    bio TEXT
);

-- 2. Create a "hidden" table with sensitive info for exfiltration
CREATE TABLE IF NOT EXISTS flags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value VARCHAR(255),
);

INSERT INTO users (username, role, bio) VALUES 
('admin', 'superuser', 'System administrator. I like long walks and securing servers.'),
('alice', 'developer', 'Full-stack dev. Don''t ask me about CSS.'),
('bob', 'hr_manager', 'I handle the people stuff. Please stop pining the database.')
('andy', 'scrum_master', 'I am perfection');

INSERT INTO flags (name, value) VALUES 
('andy', 'FLAG{absolutelySufferingFromNarcissism}');