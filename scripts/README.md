# Scripts

This directory contains lab setup and verification scripts used in the Northstar Web Application Security Assessment.

> **Authorized lab use only:** Run these scripts only against the isolated Northstar training application and fictional lab data. Do not run them against production, public, external, or real-user systems.

---

## Contents

| File | Purpose |
|---|---|
| `lab_setup.py` | Initializes or seeds the local SQLite lab database with fictional users and tickets. |
| `verify_idor_fix.py` | Performs a controlled regression check for the ticket IDOR remediation. |
| `session_cookie_check.py` | Inspects session-cookie attributes returned by the login endpoint. |

---

## Prerequisites

- Python 3.10 or later.
- A running local Northstar lab application.
- The Python `requests` package for the HTTP verification scripts.

Install the Python dependency:

```bash
pip install requests
```

Run the scripts from the repository root so relative paths resolve correctly:

```bash
python scripts/<script_name>.py
```

---

## `lab_setup.py`

### Purpose

Initializes the SQLite lab database with fictional users and support-ticket records used for local testing.

### Usage

```bash
python scripts/lab_setup.py
```

### Expected database location

```text
instance/supporthub.sqlite
```

### Notes

The script is intended for a local lab database only. Confirm that its schema matches the current Northstar application before using it, particularly if the application stores passwords or user fields differently.

---

## `verify_idor_fix.py`

### Purpose

Performs a controlled authorization regression test for the IDOR finding documented as **F-01** in the security assessment report.

The script:

1. Authenticates as each configured fictional lab user.
2. Requests each configured ticket using every authenticated user session.
3. Treats an owner’s access to their own ticket as successful only when the server returns `HTTP 200`.
4. Treats a cross-user request as successfully blocked only when the server returns `HTTP 403` or `HTTP 404`.
5. Prints `PASS` or `FAIL` for each authorization check.

### Safety control

The script rejects non-loopback targets. `BASE_URL` must use one of these local hosts:

- `127.0.0.1`
- `localhost`
- `::1`

The default target is:

```python
BASE_URL = "http://127.0.0.1:5000"
```

### Lab users

The script is configured to match the fictional users shown in the authorized lab SQLite evidence:

| User ID | Username | Email |
|---:|---|---|
| 1 | `alice.morgan` | `alice.morgan@example.invalid` |
| 2 | `robert.chen` | `robert.chen@example.invalid` |
| 3 | `dana.brooks` | `dana.brooks@example.invalid` |

Before running the script, replace the password placeholders in `verify_idor_fix.py` with the valid **fictional lab passwords**:

```python
"password": "REPLACE_WITH_ALICE_PASSWORD"
"password": "REPLACE_WITH_ROBERT_PASSWORD"
"password": "REPLACE_WITH_DANA_PASSWORD"
```

### Confirm ticket ownership first

The SQLite users screenshot establishes user IDs and email addresses, but ticket ownership must be confirmed independently. Run:

```bash
sqlite3 instance/supporthub.sqlite \
"SELECT id, owner_user_id, title FROM tickets;"
```

Then ensure the `TICKETS` mapping in `verify_idor_fix.py` matches the query output. The default mapping assumes:

```python
TICKETS = {
    "alice.morgan": 1,
    "robert.chen": 2,
    "dana.brooks": 3,
}
```

For example, if Ticket 2 belongs to Dana rather than Robert, revise the mapping before running the check. Do not claim remediation is verified until the mapping reflects the actual local database.

### Usage

```bash
python scripts/verify_idor_fix.py
```

### Expected secure result

After a correct server-side ownership check is implemented, the output should resemble:

```text
[PASS] alice.morgan accessing own ticket #1 -> HTTP 200 (expected 200)
[PASS] alice.morgan accessing robert.chen's ticket #2 -> HTTP 403 (expected 403 or 404)
[PASS] alice.morgan accessing dana.brooks's ticket #3 -> HTTP 403 (expected 403 or 404)
...
[+] IDOR remediation verification PASSED.
```

A cross-user `HTTP 200` result indicates that object-level authorization may still be missing or incorrectly implemented.

---

## `session_cookie_check.py`

### Purpose

Logs in with a fictional lab account and inspects the `Set-Cookie` response header for recommended session-cookie attributes:

- `HttpOnly`
- `Secure`
- `SameSite`

### Usage

```bash
python scripts/session_cookie_check.py
```

### Configuration

Update `BASE_URL` and the configured fictional test-user credentials in the script to match the local lab. Use only a loopback address such as `http://127.0.0.1:5000`.

### Interpretation

In the original HTTP-based lab, the observed cookie included `HttpOnly` but did not visibly include `Secure` or `SameSite`. In a production HTTPS deployment, a session cookie should normally use `HttpOnly`, `Secure`, and an appropriate `SameSite` policy such as `Lax` or `Strict`.

---

## Limitations

These scripts provide targeted, repeatable checks. They do not replace full manual testing or a complete security review.

- `verify_idor_fix.py` tests only the configured users, ticket IDs, and `GET /tickets/<id>` route.
- `session_cookie_check.py` checks visible login-response cookie attributes only.
- `lab_setup.py` depends on the local database schema matching the script assumptions.

For full scope, test limitations, and evidence references, see:

- [`../report/Northstar_Web_Application_Security_Assessment_Report.pdf`](../report/Northstar_Web_Application_Security_Assessment_Report.pdf)
- [`../docs/test_limitations.md`](../docs/test_limitations.md)
- [`../docs/evidence_index.md`](../docs/evidence_index.md)

---

## Security Note

All content in this directory supports a fictional, isolated, educational lab. Never use these scripts with real credentials, production databases, or systems that you do not explicitly own or have written authorization to test.