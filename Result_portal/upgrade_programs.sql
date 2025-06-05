-- Add program_id column to students table
ALTER TABLE students ADD COLUMN program_id INT NOT NULL AFTER program;

-- Update program_id based on matching program names
UPDATE students s
JOIN programs p ON s.program = p.name
SET s.program_id = p.id;

-- Add foreign key constraint
ALTER TABLE students
ADD CONSTRAINT fk_students_programs
FOREIGN KEY (program_id) REFERENCES programs(id);

-- Drop the old program column
ALTER TABLE students DROP COLUMN program;

-- Add index for better performance
ALTER TABLE students ADD INDEX idx_program_id (program_id);
