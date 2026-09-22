"""
Northstar Support — Intentionally Vulnerable Flask Training Application

A local-only Flask application used to demonstrate the Northstar Web
Application Security Assessment portfolio. The application includes an
intentional insecure direct object reference (IDOR) vulnerability at:

    GET /tickets/<ticket_id>

The vulnerability is deliberate so that the assessment evidence and the
IDOR verification script have a reproducible training target.

SECURITY WARNING
----------------
This application is intentionally insecure. Run it only in an isolated,
local, authorized lab environment using fictional data. It binds to
127.0.0.1 and must never be exposed to a network or deployed to production.

Quick start (from repository root):

    python scripts/lab_setup.py
    python northstar_app/northstar_app.py

Then browse to:

    http://127.0.0.1:5000

Fictional demo accounts:

    alice.morgan@example.invalid   / LabAlice-2026!
    robert.chen@example.invalid    / LabRobert-2026!
    dana.brooks@example.invalid    / LabAdmin-2026!

The SQLite database is created by scripts/lab_setup.py at:

    northstar_app/instance/supporthub_demo.sqlite
"""

from __future__ import annotations

import hashlib
import sqlite3
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

from flask import Flask, abort, redirect, render_template_string, request, session, url_for


APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "instance" / "supporthub_demo.sqlite"

app = Flask(__name__)

# Deliberately static lab-only secret. Never use this approach in production.
app.config.update(
    SECRET_KEY="northstar-intentionally-insecure-lab-secret",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE=None,
)

F = TypeVar("F", bound=Callable[..., object])


BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} | Northstar Support</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.5;
    }
    body { max-width: 960px; margin: 0 auto; padding: 2rem 1rem 3rem; color: #1f2937; }
    header { border-bottom: 2px solid #1d4ed8; margin-bottom: 1.5rem; padding-bottom: .75rem; }
    h1 { color: #1e3a8a; margin: 0; }
    h2 { color: #1e40af; }
    nav { margin-top: .5rem; }
    nav a { margin-right: .75rem; }
    .identity { color: #4b5563; font-size: .95rem; }
    .notice { background: #fef3c7; border-left: 4px solid #d97706; padding: .75rem; }
    .error { color: #b91c1c; font-weight: 600; }
    .card { border: 1px solid #d1d5db; border-radius: .5rem; padding: 1rem; margin: 1rem 0; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { border: 1px solid #d1d5db; padding: .65rem; text-align: left; vertical-align: top; }
    th { background: #eff6ff; }
    label { display: block; margin: .75rem 0 .25rem; font-weight: 600; }
    input { box-sizing: border-box; width: 100%; max-width: 420px; padding: .5rem; }
    button { background: #1d4ed8; border: 0; border-radius: .25rem; color: white; cursor: pointer; margin-top: 1rem; padding: .6rem 1rem; }
    code { background: #f3f4f6; border-radius: .2rem; padding: .1rem .25rem; }
  </style>
</head>
<body>
  <header>
    <h1>Northstar Support</h1>
    <div class="identity">Local portfolio training application — fictional data only</div>
    <nav>
      {% if session.get('user_id') %}
        <a href="{{ url_for('dashboard') }}">Dashboard</a>
        {% if session.get('role') == 'admin' %}
          <a href="{{ url_for('admin_dana') }}">Admin</a>
        {% endif %}
        <a href="{{ url_for('logout') }}">Logout</a>
        <span class="identity">Signed in as {{ session.get('username') }} ({{ session.get('role') }})</span>
      {% else %}
        <a href="{{ url_for('login') }}">Login</a>
      {% endif %}
    </nav>
  </header>

  {% if warning %}
    <div class="notice">{{ warning }}</div>
  {% endif %}

  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}

  {{ body | safe }}
</body>
</html>
"""


def render_page(title: str, body: str, *, error: str | None = None, warning: str | None = None):
    """Render an inline page inside the common local-lab layout."""
    return render_template_string(
        BASE_TEMPLATE,
        title=title,
        body=body,
        error=error,
        warning=warning,
    )


def get_db() -> sqlite3.Connection:
    """Open the dedicated local portfolio database."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Demo database not found: {DB_PATH}. Run 'python scripts/lab_setup.py' first."
        )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def hash_password(email: str, password: str) -> str:
    """Lab-only password hashing scheme; intentionally not production appropriate."""
    return hashlib.sha256(f"{email}:{password}".encode("utf-8")).hexdigest()


def login_required(view: F) -> F:
    """Redirect unauthenticated local-lab users to the login route."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


def admin_required(view: F) -> F:
    """Restrict a local demonstration route to the app-only admin account."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


@app.errorhandler(403)
def forbidden(_error):
    body = """
    <main>
      <h2>403 Forbidden</h2>
      <p>You do not have permission to access this administrative resource.</p>
      <p><a href="/dashboard">Return to the dashboard</a></p>
    </main>
    """
    return render_page("Forbidden", body), 403


@app.errorhandler(404)
def not_found(_error):
    body = """
    <main>
      <h2>404 Not Found</h2>
      <p>The requested resource could not be found.</p>
      <p><a href="/dashboard">Return to the dashboard</a></p>
    </main>
    """
    return render_page("Not Found", body), 404


@app.errorhandler(FileNotFoundError)
def database_missing(error):
    body = """
    <main>
      <h2>Local Demo Database Not Found</h2>
      <p>Initialize the fictional demo database before starting the application:</p>
      <pre><code>python scripts/lab_setup.py</code></pre>
    </main>
    """
    return render_page("Database Setup Required", body, error=str(error)), 500


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = """
    <main>
      <h2>Sign In</h2>
      <p>Use a fictional local-lab account. This application is intentionally vulnerable for training.</p>
      <form method="post" autocomplete="off">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required>

        <label for="password">Password</label>
        <input id="password" name="password" type="password" required>

        <button type="submit">Sign In</button>
      </form>
    </main>
    """

    if request.method == "GET":
        return render_page("Login", form, warning="Local lab only. Do not enter real credentials.")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    with get_db() as connection:
        user = connection.execute(
            """
            SELECT id, name, username, email, password_hash, role
            FROM users
            WHERE email = ? AND password_hash = ?
            """,
            (email, hash_password(email, password)),
        ).fetchone()

    if user is None:
        return render_page(
            "Login",
            form,
            error="Invalid email or password.",
            warning="Local lab only. Do not enter real credentials.",
        ), 401

    # The app intentionally does not regenerate its client-side session identifier.
    # This is retained for session-management testing in the authorized lab.
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["name"] = user["name"]
    session["role"] = user["role"]

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    with get_db() as connection:
        tickets = connection.execute(
            """
            SELECT id, title, priority, status, created_at
            FROM tickets
            WHERE owner_user_id = ?
            ORDER BY id
            """,
            (session["user_id"],),
        ).fetchall()

    ticket_rows = "".join(
        "<tr>"
        f"<td><a href='{url_for('ticket_detail', ticket_id=ticket['id'])}'>{ticket['id']}</a></td>"
        f"<td>{ticket['title']}</td>"
        f"<td>{ticket['priority']}</td>"
        f"<td>{ticket['status']}</td>"
        "</tr>"
        for ticket in tickets
    ) or "<tr><td colspan='4'>No tickets found.</td></tr>"

    body = f"""
    <main>
      <h2>Dashboard</h2>
      <div class="card">
        <p>Welcome, <strong>{session.get('name')}</strong>.</p>
        <p>Your account is a <code>{session.get('role')}</code> account.</p>
      </div>
      <h3>Your Tickets</h3>
      <table>
        <thead><tr><th>ID</th><th>Title</th><th>Priority</th><th>Status</th></tr></thead>
        <tbody>{ticket_rows}</tbody>
      </table>
    </main>
    """
    return render_page("Dashboard", body)


@app.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id: int):
    """
    INTENTIONALLY VULNERABLE — DO NOT COPY INTO PRODUCTION.

    The route retrieves a ticket by its numeric ID but deliberately does not
    check ticket.owner_user_id against session['user_id']. An authenticated
    user can request another user's ticket by changing the URL identifier.

    This reproduces F-01 (IDOR / Broken Access Control) in the portfolio.
    """
    with get_db() as connection:
        ticket = connection.execute(
            """
            SELECT id, title, description, owner_user_id, assigned_user_id,
                   priority, status, created_at
            FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if ticket is None:
        abort(404)

    body = f"""
    <main>
      <h2>Ticket #{ticket['id']}</h2>
      <div class="card">
        <p><strong>Title:</strong> {ticket['title']}</p>
        <p><strong>Description:</strong> {ticket['description']}</p>
        <p><strong>Priority:</strong> {ticket['priority']}</p>
        <p><strong>Status:</strong> {ticket['status']}</p>
        <p><strong>Owner User ID:</strong> {ticket['owner_user_id']}</p>
        <p><strong>Assigned User ID:</strong> {ticket['assigned_user_id']}</p>
        <p><strong>Created At:</strong> {ticket['created_at']}</p>
      </div>
      <p><a href="{url_for('dashboard')}">Return to dashboard</a></p>
    </main>
    """
    return render_page("Ticket Detail", body)


@app.route("/admin/dana")
@admin_required
def admin_dana():
    """Protected route retained to demonstrate a successful vertical-access-control check."""
    body = """
    <main>
      <h2>Administrator Panel</h2>
      <div class="card">
        <p>This local demonstration route requires the app-only administrator role.</p>
        <p>It is intentionally separate from the vulnerable ticket-detail route.</p>
      </div>
    </main>
    """
    return render_page("Administrator Panel", body)


if __name__ == "__main__":
    if not DB_PATH.exists():
        print("[!] Demo database not found.")
        print("[!] From the repository root, run: python scripts/lab_setup.py")
    else:
        print("[*] Northstar Support local training application")
        print("[*] URL: http://127.0.0.1:5000")
        print("[!] Intentionally vulnerable. Local lab use only.")

    # Binding explicitly to loopback prevents network exposure.
    app.run(host="127.0.0.1", port=5000, debug=True)
