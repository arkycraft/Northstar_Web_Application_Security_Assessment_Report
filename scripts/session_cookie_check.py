"""
Session Cookie Security Check (Lab Only)

This script logs in to the Northstar Support lab application and inspects
the session cookie attributes returned by the login endpoint.

It checks for:
- HttpOnly
- Secure
- SameSite

WARNING:
- Run this ONLY against a local lab instance (e.g., http://127.0.0.1:5000).
- Do NOT run against any production or external system.
- This script is for educational / training purposes only.

Usage:

    python scripts/session_cookie_check.py

Adjust BASE_URL and credentials to match your local lab.
"""

import requests
from urllib.parse import urljoin

# CHANGE THIS ONLY TO MATCH YOUR LOCAL LAB; DO NOT POINT TO PRODUCTION
BASE_URL = "http://127.0.0.1:5000"

# Fictional lab credentials (must match your lab data)
TEST_USER = {
    "email": "alice.morgan@example.invalid",
    "password": "LabAlice-2026!",  # adjust to match your lab
}


def inspect_session_cookie():
    """Log in and inspect the Set-Cookie header for session security attributes."""
    print("[*] Session Cookie Security Check (Lab Only)")
    print(f"[*] Target: {BASE_URL}")
    print()

    session = requests.Session()
    login_url = urljoin(BASE_URL, "/login")

    resp = session.post(
        login_url,
        data={"email": TEST_USER["email"], "password": TEST_USER["password"]},
        allow_redirects=False,
    )

    if resp.status_code not in (200, 302):
        print(f"[!] Login failed: {resp.status_code}")
        print("[!] Check credentials and ensure the lab is running.")
        return

    # Inspect Set-Cookie headers
    set_cookie_headers = resp.headers.getlist("Set-Cookie")
    if not set_cookie_headers:
        print("[!] No Set-Cookie header found in login response.")
        return

    print("[+] Login successful.")
    print()

    session_cookie = None
    for header in set_cookie_headers:
        if "session" in header.lower():
            session_cookie = header
            break

    if not session_cookie:
        print("[!] No 'session' cookie found in Set-Cookie headers.")
        print("[*] Raw Set-Cookie headers:")
        for h in set_cookie_headers:
            print("  ", h)
        return

    print("[+] Session cookie found:")
    print("  ", session_cookie)
    print()

    # Normalize for checking
    cookie_lower = session_cookie.lower()

    checks = {
        "HttpOnly": "httponly" in cookie_lower,
        "Secure": "secure" in cookie_lower,
        "SameSite": "samesite" in cookie_lower,
    }

    print("[*] Attribute checks:")
    for attr, present in checks.items():
        status = "Present" if present else "Missing"
        symbol = "[+]" if present else "[!]"
        print(f"  {symbol} {attr}: {status}")

    print()

    # Simple interpretation
    if checks["HttpOnly"] and checks["Secure"] and checks["SameSite"]:
        print("[+] Session cookie appears well-hardened for HTTPS deployment:")
        print("    HttpOnly, Secure, and SameSite are all present.")
    else:
        print("[!] Session cookie is missing one or more recommended attributes.")
        print("[!] For production over HTTPS, you typically want:")
        print("    - HttpOnly")
        print("    - Secure")
        print("    - SameSite=Lax or Strict")
        print()
        print("[*] In a local HTTP lab, Secure may be omitted intentionally,")
        print("    but production deployments should enable it with HTTPS.")

    print()
    print("[*] This is a basic automated check only.")
    print("[*] It does not replace a full session-management review.")


if __name__ == "__main__":
    inspect_session_cookie()