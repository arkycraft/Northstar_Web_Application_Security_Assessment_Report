# Database – Northstar Support

This directory contains the SQLite schema and seed data for the **Northstar Support** lab application.

**Warning:**  
These scripts are for **isolated lab use only**. Do not run them against production systems or real user data.

---

## Files

- `supporthub_schema.sql`  
  Defines the `users` and `tickets` tables and a simple index.

- `supporthub_seed.sql`  
  Inserts fictional test users and tickets used in the security assessment.

---

## How to Use

### Option 1 – Let the Flask app create the database

The easiest way is to run the Flask app once:

```bash
cd northstar_app
python northstar_app.py
```

On first run, it will:

- Create `instance/supporthub.sqlite`.
- Create the schema.
- Seed fictional users and tickets automatically.

You can then inspect the database with:

```bash
sqlite3 instance/supporthub.sqlite
```

### Option 2 – Manually create and seed the database

From this `database/` directory:

```bash
# Create a new database file
sqlite3 supporthub.db < supporthub_schema.sql

# Insert seed data
sqlite3 supporthub.db < supporthub_seed.sql
```

You can then point the Flask app to this file by adjusting `DB_PATH` in `northstar_app.py`, or copy `supporthub.db` into `northstar_app/instance/`.

---

## Schema Overview

### `users` table

- `id` – Primary key.
- `name` – User’s display name (e.g., “Alice”).
- `email` – Unique login identifier.
- `password_hash` – Hashed password (lab-only hashing scheme).
- `role` – Either `user` or `admin`.

### `tickets` table

- `id` – Primary key.
- `title` – Short summary of the support request.
- `description` – Detailed description.
- `owner_user_id` – User who created the ticket.
- `assigned_user_id` – User assigned to work on the ticket (can be NULL).
- `priority` – e.g., `low`, `medium`, `high`.
- `status` – e.g., `open`, `closed`.
- `created_at` – Timestamp of ticket creation.

---

## Security Notes

- The password hashing used in the accompanying Flask app is **not secure** and is only for demonstration.
- This schema does not include production-grade constraints, auditing columns, or security controls.
- Use this only with fictional data in a controlled lab environment.