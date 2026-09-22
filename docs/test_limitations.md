# Appendix B: Test Limitations

The following limitations define the depth and interpretation of this assessment.

---

## B.1 Scope and Coverage

- The assessment was time-boxed and focused on high-impact web-application controls, mainly authentication, session management, and authorization.
- Not every endpoint, HTTP method, parameter, user role, workflow, or error condition was exhaustively tested.
- The assessment was conducted against the specified Northstar lab deployment; findings may not apply unchanged to another environment or production deployment.

---

## B.2 Input Validation

- SQL injection testing consisted of basic screening on the login flow and selected inputs. Blind, time-based, second-order, and database-specific techniques were not comprehensively tested.
- XSS testing consisted of basic reflected-input screening. Stored XSS, DOM-based XSS, and context-specific encoding bypasses were not comprehensively assessed.
- CSRF defenses were not subject to dedicated, end-to-end validation.

---

## B.3 Authentication and Sessions

- Password-storage details, including hashing algorithm, salt use, work factor, and password-reset flow security, were not independently verified.
- Intruder testing was limited to avoid account lockout, excessive authentication traffic, and disruption. A large-scale credential attack was not performed.
- Cookie behavior was evaluated from observed HTTP responses; infrastructure-level TLS termination, reverse-proxy configuration, and production security controls were not independently reviewed.

---

## B.4 Authorization and Environment

- Access-control testing confirmed the documented ticket IDOR scenario, but it did not constitute exhaustive authorization testing across every resource type.
- Administrative functionality was tested only at the endpoint(s) available within the approved scope. The observed `403 Forbidden` result is evidence for that tested route only.
- Internal network segmentation, host hardening, source-code review, dependency analysis, cloud configuration review, and post-compromise activities were outside this web assessment's scope.

---

## B.5 Interpretation

Negative results mean that no vulnerability was identified through the techniques and coverage described above. They do not demonstrate that the application is free of vulnerabilities in those categories.