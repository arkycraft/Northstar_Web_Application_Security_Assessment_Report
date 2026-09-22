# Evidence Directory

This directory contains the raw evidence screenshots and companion documentation files supporting the findings in the [Northstar Web Application Security Assessment Report](../report/Northstar_Web_Application_Security_Assessment_Report.pdf).

## Structure

Evidence is organized by testing phase to match Appendix A of the report:

```text
evidence/
├── 01_recon/                 # Reconnaissance and scope definition
├── 02_authentication/        # Authentication testing (login, Intruder)
├── 03_session_management/    # Session-cookie and logout testing
└── 04_authorization/         # Authorization and IDOR testing
```

## File Naming Convention

Each screenshot has a companion `.md` file with the same base name:

- `XXX_description.jpg` – The actual screenshot captured during testing.
- `XXX_description.md` – A short description of the figure, its purpose, and where it appears in the report.

Example:

- `3-1_inspect_set_cookie_header.jpg` – Screenshot of the `Set-Cookie` header.
- `3-1_inspect_set_cookie_header.md` – Description of Figure 9 and its context.

## How to Use This Directory

- **For reviewers:** Open the PDF report and refer to the figure numbers. Use this directory to inspect the original, full-resolution screenshots.
- **For learners:** Read the `.md` files to understand what each screenshot demonstrates and how it supports a specific finding or test case.
- **For auditors:** The `.md` files provide traceability from report figures back to raw evidence.

## Mapping to Report Figures

See [`../docs/evidence_index.md`](../docs/evidence_index.md) for a complete mapping of report figure numbers to files in this directory.

## Notes

- All screenshots were captured in an isolated lab environment using authorized test accounts and fictional data.
- No production systems or real user data were accessed during testing.