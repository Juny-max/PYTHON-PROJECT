-- First get the level IDs
SET @level100 = (SELECT id FROM levels WHERE name = 'Level 100');
SET @level200 = (SELECT id FROM levels WHERE name = 'Level 200');
SET @level300 = (SELECT id FROM levels WHERE name = 'Level 300');
SET @level400 = (SELECT id FROM levels WHERE name = 'Level 400');

-- Update student level IDs (you may need to adjust this based on your actual student data)
UPDATE students SET level_id = @level100 WHERE archived = FALSE;

-- You can manually update specific students if needed:
-- UPDATE students SET level_id = @level200 WHERE id = <student_id>;
-- UPDATE students SET level_id = @level300 WHERE id = <student_id>;
-- UPDATE students SET level_id = @level400 WHERE id = <student_id>;
