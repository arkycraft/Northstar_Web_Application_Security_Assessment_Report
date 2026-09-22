"""
Northstar Support — IDOR Remediation Verification (Lab Only)

Performs a controlled authorization regression test against the local
Northstar Support training application.

The script:
- Authenticates as each fictional lab user.
- Requests each configured ticket as every authenticated user.
- Verifies that a user can access their own ticket (expected: HTTP 200).
- Verifies that cross-user ticket access is denied (expected: HTTP 403 or 404).

Safety:
- This script is restricted to loopback addresses.
- Run it only against the isolated, authorized Northstar lab.
- Do not use it against production, external, or real-user systems.

Usage:
    python scripts/verify_idor_fix.py

Prerequisites:
    pip install requests

Before running:
    1. Start the local Northstar application.
    2. Confirm valid test credentials.
    3. Confirm ticket ownership:

       sqlite3 instance/supporthub.sqlite \
       "SELECT id, owner_user_id, title FROM tickets;"
"""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests


BASE_URL = "http://127.0.0.1:5000"

# Actual fictional users shown in the authorized lab SQLite screenshot.
# Replace only the password placeholders with valid local-lab credentials.
USERS = {
    "alice.morgan": {
        "email": "alice.morgan@example.invalid",
        "password": "REPLACE_WITH_ALICE_PASSWORD",
    },
    "robert.chen": {
        "email": "robert.chen@example.invalid",
        "password": "REPLACE_WITH_ROBERT_PASSWORD",
    },
    "dana.brooks": {
        "email": "dana.brooks@example.invalid",
        "password": "REPLACE_WITH_DANA_PASSWORD",
    },
}

# Confirm ticket ownership with:
# sqlite3 instance/supporthub.sqlite \
# "SELECT id, owner_user_id, title FROM tickets;"
#
# This assumes the normal lab mapping:
# ticket 1 -> owner_user_id 1 -> alice.morgan
# ticket 2 -> owner_user_id 2 -> robert.chen
# ticket 3 -> owner_user_id 3 -> dana.brooks
TICKETS = {
    "alice.morgan": 1,
    "robert.chen": 2,
    "dana.brooks": 3,
}

SUCCESS_CODES = {200}
DENIED_CODES = {403, 404}


def assert_local_target(base_url: str) -> None:
    """Refuse targets other than local loopback HTTP/HTTPS addresses."""
    parsed = urlparse(base_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("BASE_URL must start with http:// or https://")

    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError(
            "Safety check failed: BASE_URL must use localhost, 127.0.0.1, or ::1."
        )


def login(email: str, password: str) -> requests.Session:
    """Authenticate a fictional lab user and return the session."""
    session = requests.Session()
    response = session.post(
        urljoin(BASE_URL, "/login"),
        data={"email": email, "password": password},
        allow_redirects=False,
        timeout=10,
    )

    if response.status_code not in {200, 302, 303}:
        raise RuntimeError(f"Login failed for {email}: HTTP {response.status_code}")

    if not session.cookies:
        raise RuntimeError(
            f"Login response for {email} did not establish a session cookie."
        )

    return session


def get_ticket_status(session: requests.Session, ticket_id: int) -> int:
    """Request a ticket and return only the HTTP response status."""
    response = session.get(
        urljoin(BASE_URL, f"/tickets/{ticket_id}"),
        allow_redirects=False,
        timeout=10,
    )
    return response.status_code


def main() -> None:
    """Run controlled cross-user authorization checks."""
    assert_local_target(BASE_URL)

    print("[*] Northstar IDOR Remediation Verification — Lab Only")
    print(f"[*] Target: {BASE_URL}")
    print()

    if any(user["password"].startswith("REPLACE_WITH_") for user in USERS.values()):
        print("[!] Update the placeholder password values in USERS before running.")
        return

    sessions: dict[str, requests.Session] = {}

    for username, credentials in USERS.items():
        try:
            sessions[username] = login(
                credentials["email"],
                credentials["password"],
            )
            print(f"[+] Authenticated as {username}")
        except (requests.RequestException, RuntimeError) as exc:
            print(f"[!] Could not authenticate as {username}: {exc}")
            return

    print("\n[*] Authorization results:\n")

    failures = []
    passed = 0
    total = 0

    for actor, session in sessions.items():
        for ticket_owner, ticket_id in TICKETS.items():
            total += 1
            status = get_ticket_status(session, ticket_id)
            is_own_ticket = actor == ticket_owner

            if is_own_ticket:
                expected = "200"
                outcome = status in SUCCESS_CODES
                description = f"{actor} accessing own ticket #{ticket_id}"
            else:
                expected = "403 or 404"
                outcome = status in DENIED_CODES
                description = f"{actor} accessing {ticket_owner}'s ticket #{ticket_id}"

            result = "PASS" if outcome else "FAIL"
            print(f"[{result}] {description} -> HTTP {status} (expected {expected})")

            if outcome:
                passed += 1
            else:
                failures.append(
                    {
                        "actor": actor,
                        "ticket_owner": ticket_owner,
                        "ticket_id": ticket_id,
                        "status": status,
                        "expected": expected,
                    }
                )

    print(f"\n[*] Completed {total} checks: {passed} passed, {len(failures)} failed.")

    if failures:
        print("\n[!] IDOR remediation verification FAILED.")
        print("[!] Review these unexpected results:")

        for failure in failures:
            print(
                "    - "
                f"{failure['actor']} -> ticket #{failure['ticket_id']} "
                f"owned by {failure['ticket_owner']}: HTTP {failure['status']} "
                f"(expected {failure['expected']})"
            )

        print(
            "\n[!] A cross-user HTTP 200 response indicates that object-level "
            "authorization may still be missing or incorrectly implemented."
        )
    else:
        print("\n[+] IDOR remediation verification PASSED.")
        print(
            "[+] All users accessed their configured own ticket, while "
            "cross-user ticket requests were denied."
        )

    print(
        "\n[*] This is a limited regression check, not a substitute for a full "
        "authorization review."
    )


if __name__ == "__main__":
    main()
