-- SQL to add password_changed column to users table
ALTER TABLE users 
ADD COLUMN password_changed BOOLEAN NOT NULL DEFAULT FALSE 
COMMENT 'Flag to track if user has changed their password';

-- Update existing users to have password_changed = TRUE
-- (assuming existing users have already logged in with their passwords)
UPDATE users SET password_changed = TRUE;

-- For new students, we'll set password_changed = FALSE when creating their accounts
-- This is handled in the Python code we've already updated
