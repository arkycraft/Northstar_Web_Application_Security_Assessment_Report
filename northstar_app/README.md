# Northstar Support – Flask Lab Application

This is a minimal, intentionally vulnerable Flask application used for the **Northstar Web Application Security Assessment** portfolio. It simulates a basic support-ticket system with login, dashboard, ticket details, and an admin route.

**Security warning:**  
This application is **intentionally insecure** and must **never** be deployed to production or exposed to the public internet. It is for **local lab and educational use only**.

---

## Features

- User login/logout with session cookies.
- Dashboard showing a user’s tickets.
- Ticket detail endpoint with a **deliberate IDOR vulnerability** for training.
- Simple admin-only route (`/admin/dana`) that enforces role-based access.
- SQLite database for users and tickets.

---

## Quick Start (Local Lab)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-root>/northstar_app
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python northstar_app.py
```

The app will:

- Create `instance/supporthub.sqlite` if it does not exist.
- Seed fictional users and tickets.
- Start on `http://127.0.0.1:5000`.

### 5. Log in with test accounts

Use these fictional credentials (for lab only):

- **Alice (standard user)**  
  - Email: `alice.morgan@example.invalid`  
  - Password: `LabAlice-2026!`

- **Robert (standard user)**  
  - Email: `robert.chen@example.invalid`  
  - Password: `LabRobert-2026!`

- **Dana (administrator)**  
  - Email: `dana.brooks@example.invalid`  
  - Password: `LabAdmin-2026!`

---

## Intended Use

This app is designed to:

- Demonstrate common web vulnerabilities (e.g., IDOR) in a controlled environment.
- Support security-testing exercises such as:
  - Authorization testing (horizontal and vertical privilege escalation).
  - Session-management testing.
  - Basic input-validation checks.

It is **not** intended to:

- Be secure, hardened, or production-ready.
- Handle real user data or sensitive information.

---

## Security Notes

- Run this only on `127.0.0.1` or in an isolated VM/network.
- Do not expose this application to the internet.
- Do not use real credentials or personal data.
- The password hashing used here is **for lab demonstration only** and is not suitable for production.

---

## Relation to Portfolio

This application is the target of the security assessment documented in:

- [`../report/Northstar_Web_Application_Security_Assessment_Report.pdf`](../report/Northstar_Web_Application_Security_Assessment_Report.pdf)

The report describes:

- The testing methodology.
- Confirmed findings (including the IDOR in `/tickets/<id>`).
- Remediation recommendations.

Use this app to:

- Reproduce the findings in your own lab.
- Practice applying the recommended fixes.
- Extend the app with additional features and re-test.