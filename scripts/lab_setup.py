"""
Northstar Support — Local Lab Database Setup

Creates and seeds a dedicated SQLite database for the runnable Northstar
portfolio application using fictional data only.

This script intentionally creates a separate demo database so the original
assessment evidence database is not modified.

Safety:
- For isolated, authorized, educational lab use only.
- Do not run against production databases or real user data.
- The generated passwords and hashing scheme are demonstration-only.

Usage:
    python scripts/lab_setup.py

Optional reset of the dedicated demo database:
    python scripts/lab_setup.py --reset

The default output database is:
    northstar_app/instance/supporthub_demo.sqlite
"""

from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "northstar_app" / "instance" / "supporthub_demo.sqlite"


USERS = [
    {
        "id": 1,
        "name": "Alice Morgan",
        "username": "alice.morgan",
        "email": "alice.morgan@example.invalid",
        "password": "LabAlice-2026!",
        "role": "user",
    },
    {
        "id": 2,
        "name": "Robert Chen",
        "username": "robert.chen",
        "email": "robert.chen@example.invalid",
        "password": "LabRobert-2026!",
        "role": "user",
    },
    {
        "id": 3,
        "name": "Dana Brooks",
        "username": "dana.brooks",
        "email": "dana.brooks@example.invalid",
        "password": "LabAdmin-2026!",
        "role": "user",
    },
   
]


TICKETS = [
    {
        "id": 1,
        "title": "Alice cannot access dashboard",
        "description": "Alice reports a 403 response while accessing /dashboard.",
        "owner_user_id": 1,
        "assigned_user_id": 1,
        "priority": "high",
        "status": "open",
    },
    {
        "id": 2,
        "title": "Robert cannot update account contact details",
        "description": "Robert reports that profile changes do not persist.",
        "owner_user_id": 2,
        "assigned_user_id": 2,
        "priority": "medium",
        "status": "open",
    },
    {
        "id": 3,
        "title": "Dana password reset not working",
        "description": "Dana did not receive a password-reset email.",
        "owner_user_id": 3,
        "assigned_user_id": 3,
        "priority": "medium",
        "status": "open",
    },
]


def hash_password(email: str, password: str) -> str:
    """Return a deterministic lab-only SHA-256 password hash."""
    value = f"{email}:{password}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the schema used by the dedicated demo application database."""
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('user', 'admin'))
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            owner_user_id INTEGER NOT NULL,
            assigned_user_id INTEGER,
            priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
            status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_user_id) REFERENCES users(id),
            FOREIGN KEY (assigned_user_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_tickets_owner_user_id
            ON tickets(owner_user_id);
        """
    )


def seed_data(connection: sqlite3.Connection) -> None:
    """Insert deterministic fictional users and tickets into the demo database."""
    user_rows = [
        (
            user["id"],
            user["name"],
            user["username"],
            user["email"],
            hash_password(user["email"], user["password"]),
            user["role"],
        )
        for user in USERS
    ]

    connection.executemany(
        """
        INSERT OR REPLACE INTO users
        (id, name, username, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        user_rows,
    )

    ticket_rows = [
        (
            ticket["id"],
            ticket["title"],
            ticket["description"],
            ticket["owner_user_id"],
            ticket["assigned_user_id"],
            ticket["priority"],
            ticket["status"],
        )
        for ticket in TICKETS
    ]

    connection.executemany(
        """
        INSERT OR REPLACE INTO tickets
        (id, title, description, owner_user_id, assigned_user_id, priority, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ticket_rows,
    )


def show_summary(connection: sqlite3.Connection) -> None:
    """Print the seeded identities and ticket ownership for verification."""
    print("\n[+] Fictional users:")
    for row in connection.execute(
        "SELECT id, username, email, role FROM users ORDER BY id"
    ):
        print(f"    {row[0]} | {row[1]} | {row[2]} | {row[3]}")

    print("\n[+] Ticket ownership:")
    for row in connection.execute(
        "SELECT id, owner_user_id, title FROM tickets ORDER BY id"
    ):
        print(f"    Ticket {row[0]} | owner_user_id={row[1]} | {row[2]}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the dedicated Northstar portfolio demo database."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and recreate supporthub_demo.sqlite before seeding.",
    )
    args = parser.parse_args()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if args.reset and DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[*] Removed existing demo database: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        create_schema(connection)
        seed_data(connection)
        connection.commit()
        show_summary(connection)

    print(f"\n[+] Demo database ready: {DB_PATH}")
    print("[+] Use only with the local Northstar portfolio application.")
    print("[!] Password hashing is intentionally simplified for this lab and is not production-safe.")


if __name__ == "__main__":
    main()
