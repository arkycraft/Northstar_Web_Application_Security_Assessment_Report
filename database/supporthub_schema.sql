-- Northstar Support – SQLite Schema (Lab Only)
--
-- This SQL script defines the database schema used by the Northstar Support
-- Flask application. It is intended for educational and lab use only.
--
-- WARNING:
-- - Do NOT use this schema in production.
-- - Password hashing in the accompanying app is for demonstration only.
-- - Run this only against isolated, fictional lab data.

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);

-- Tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    owner_user_id INTEGER NOT NULL,
    assigned_user_id INTEGER,
    priority TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_user_id) REFERENCES users(id)
);

-- Optional: simple index on owner_user_id for faster ticket lookups
CREATE INDEX IF NOT EXISTS idx_tickets_owner_user_id ON tickets(owner_user_id);