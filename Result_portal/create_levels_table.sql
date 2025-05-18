-- Create levels table
CREATE TABLE IF NOT EXISTS levels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(100),
    archived BOOLEAN DEFAULT FALSE NOT NULL
);

-- Add default levels
INSERT INTO levels (name, description) VALUES
('Level 100', 'First Year Students'),
('Level 200', 'Second Year Students'),
('Level 300', 'Third Year Students'),
('Level 400', 'Fourth Year Students');
