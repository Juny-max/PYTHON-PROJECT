ALTER TABLE students ADD COLUMN level_id INT NOT NULL;
ALTER TABLE students ADD CONSTRAINT fk_level_id FOREIGN KEY (level_id) REFERENCES levels(id);
