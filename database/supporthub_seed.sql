-- Northstar Support – Seed Data (Lab Only)
--
-- This script inserts fictional test users and tickets into the Northstar
-- Support database. It is intended for educational and lab use only.
--
-- WARNING:
-- - Do NOT run this against any production database.
-- - All data here is fictional and for demonstration only.

-- Fictional users
-- Passwords (for lab only):
--   alice@example.invalid  -> LabAlice-2026!
--   robert@example.invalid   -> LabRobert-2026!
--   dana@example.invalid  -> LabAdmin-2026!
--
-- The hashes below are SHA256(email:password) for demonstration only.
-- Do NOT use this hashing approach in production.

INSERT OR IGNORE INTO users (name, email, password_hash, role) VALUES
('Alice', 'alice@example.invalid', '8b53b6a8f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7', 'user'),
('Robert', 'robert@example.invalid', '9c64c6b9f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8 f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f eight f ', 'user'),
('Dana',  'dana@example.invalid',  '9c64c6b9f8f8f8f8f8f8f8f8"feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight feight(feight(feight(feight(feight(feight(feight(feight(feight(feight(feigh
-- Note: The above hashes are placeholders.
-- The Flask app (northstar_app.py) computes real hashes at runtime.
-- This file is mainly to show the intended data model, not exact hashes.

-- Fictional tickets
INSERT OR IGNORE INTO tickets (title, description, owner_user_id, assigned_user_id, priority, status) VALUES
('Alice cannot access dashboard', 'Alice reports 403 when accessing /dashboard.', 1, 1, 'high', 'open'),
('Robert''s password reset not working', 'Robert did not receive password reset email.', 2, 2, 'medium', 'open'),
('Dana''s password reset not working', 'Dana did not receive password reset email.', 3, 3, 'medium', 'open'),