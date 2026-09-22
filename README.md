# Northstar Web Application Security Assessment – Portfolio

**Author:** Arky Craft  
**Date:** September 2026  
**Assessment type:** Authorized web application security assessment (lab environment)

---

## Overview

This repository contains a complete, OWASP-aligned web application security assessment of the **Northstar Support** ticketing application, a Flask-based training environment developed and operated solely for educational purposes. The assessment was designed, executed, and documented as part of a structured web application penetration testing and security review project.

The full report is available here:  
📄 **[Northstar_Web_Application_Security_Assessment_Report.pdf](report/Northstar_Web_Application_Security_Assessment_Report.pdf)**

---

## How to Browse This Repository

Start here based on your role or interest:

- **First-time visitors / general overview**  
  - Read this `README.md` for a high-level summary.  
  - Skim the [Key Findings](#key-findings) table.  

- **Instructors / evaluators**  
  1. Open the [PDF report](report/Northstar_Web_Application_Security_Assessment_Report.pdf).  
  2. Review the [Evidence Index](docs/evidence_index.md) to see how figures map to raw screenshots.  
  3. Optionally inspect the [Test Limitations](docs/test_limitations.md) to understand scope boundaries.  

- **Security practitioners**  
  1. Review the [Key Findings](#key-findings) and jump to the corresponding sections in the PDF.  
  2. Examine the [Evidence directory](evidence/) to inspect raw screenshots and their descriptions.  
  3. Read the [References](docs/references.md) for the OWASP and PortSwigger resources used.  

- **Students / learners**  
  1.  Read the [full assessment report](report/Northstar_Web_Application_Security_Assessment_Report.pdf), especially Section 3, “Environment and Methodology,” to understand the testing workflow.  
  2. Compare the [Test Limitations](docs/test_limitations.md) with your own assessments to see what was in/out of scope.  
  3. Explore the [evidence folders](evidence/) to see how each screenshot supports a specific finding.  

- **Auditors / reviewers**  
  1. Use the [Evidence Index](docs/evidence_index.md) to trace every figure back to its source image.  
  2. Review the [Evidence README](evidence/README.md) for file naming conventions and structure.  
  3. Cross-reference findings with the [References](docs/references.md) for methodology alignment.  

---

## Lab Environment

Testing was conducted in an isolated, assessor-controlled lab:

- **Tester workstation:** Kali Linux  
- **Target system:** Ubuntu VM hosting Northstar Support  
- **Application framework:** Python / Flask  
- **Web service:** HTTP on port 5000  
- **Database:** SQLite (`supporthub.sqlite`)  
- **Tools:** Burp Suite Community Edition, Firefox, Visual Studio Code, SQLite CLI, Linux command-line utilities  

The scope was limited to authentication, session management, authorization, input validation, error handling, security configuration, and basic monitoring controls.

---

## Key Findings

| ID   | Finding                                                      | Severity      | OWASP Top 10 (2025)            |
|------|--------------------------------------------------------------|---------------|--------------------------------|
| F-01 | Insecure Direct Object Reference (IDOR) in Ticket Endpoint   | **High**      | A01 – Broken Access Control    |
| F-02 | Incomplete Session-Cookie Security Attributes + HTTP Transport **Medium**    | A07 – Authentication Failures  |
| T-01 | SQL Injection Testing of Login Endpoint                      | Informational | A05 – Injection                |
| T-02 | Vertical Privilege Escalation at Admin Endpoint              | Informational | A01 – Broken Access Control    |
| T-03 | Reflected XSS Testing of Login Endpoint                      | Informational | A05 – Injection                |
| T-04 | CSRF Testing Limitations                                     | Informational | Session Management             |
| T-05 | Password-Storage Review Limitation                           | Informational | A07 – Authentication Failures  |

**Summary:**  
The assessment confirmed one **high-severity** broken access control vulnerability (horizontal privilege escalation / IDOR in the ticket-detail endpoint) and one **medium-severity** session-cookie hardening issue. Tests for SQL injection, reflected XSS, and vertical privilege escalation did not demonstrate exploitable weaknesses within the tested scope.

---

## Repository Contents

- `README.md` – This file; repository overview and navigation guide.  
- `portfolio_cover_note.md` – Short cover note describing the portfolio's purpose and context.  
- `report/` – Full 32-page security assessment report (PDF).  
- `docs/` – Supporting documentation:
  - `evidence_index.md` – Mapping of report figures to evidence files.
  - `test_limitations.md` – Appendix B: Test limitations.
  - `references.md` – Appendix C: References.
  - `methodology.md` – (Optional) Expanded methodology notes.  
- `evidence/` – Raw screenshots and companion `.md` files, organized by testing phase:
  - `01_recon/` – Reconnaissance and scope definition.
  - `02_authentication/` – Authentication testing (login, Intruder).
  - `03_session_management/` – Session-cookie and logout testing.
  - `04_authorization/` – Authorization and IDOR testing.  
- `scripts/` – Reserved for lab setup or automation scripts (currently empty).

The report includes:

- Executive Summary  
- Scope and Rules of Engagement  
- Lab Environment and Methodology  
- Findings Summary  
- Detailed Findings (F-01, F-02, T-01–T-05)  
- Remediation Roadmap  
- Conclusion  
- Appendices: Evidence, Test Limitations, References  

---

## Methodology

Testing followed an **OWASP Web Security Testing Guide (WSTG)**–aligned workflow:

1. Reconnaissance and application mapping (Burp Proxy, Site Map).  
2. Authentication testing (valid/invalid logins, limited brute-force, SQLi probes).  
3. Authorization testing (horizontal and vertical privilege escalation).  
4. Session-management testing (cookie attributes, tamper resistance, logout).  
5. Input validation and error handling (SQLi, reflected XSS markers, headers).  
6. Logging and monitoring (controlled failed-login and unauthorized-access events).  

See [`docs/methodology.md`](docs/methodology.md) (if present) for expanded notes.

---

## Important Notes

- All testing was performed against **fictional accounts and data** in a **non-production training lab**.  
- No external systems, production environments, or real user data were accessed or affected.  
- This portfolio is intended for **educational and demonstration purposes** only.  

---

## References

- OWASP Web Security Testing Guide (WSTG)  
- OWASP Top 10: 2025  
- OWASP Cheat Sheet Series (Authorization, IDOR Prevention, Session Management, Authentication)  
- PortSwigger Web Security Academy – Access Control Vulnerabilities  
- PortSwigger Burp Suite Documentation  

Full reference list is included in [`docs/references.md`](docs/references.md) and Appendix C of the report.