# Appendix D — Glossary

This glossary defines common web-application security terms and abbreviations used throughout this report. Definitions are written for both technical and nontechnical readers.

| Term | Definition |
|---|---|
| 200 OK | An HTTP response status indicating that a request was successfully received and processed. In this assessment, a 200 OK response to a ticket request showed that the application returned the requested ticket data. |
| 302 Found | An HTTP response status indicating that the browser should redirect to another location. Applications commonly return this response after a successful login to send the user to a dashboard or home page. |
| 403 Forbidden | An HTTP response status indicating that the server understood the request but refuses to authorize the user to access the requested resource or function. |
| 404 Not Found | An HTTP response status indicating that the requested resource could not be found. Some applications use 404 responses when a user should not be able to learn whether a protected resource exists. |
| Adaptive Password Hashing | A password-protection approach designed to be intentionally slow and configurable. Its computational cost can be increased over time as hardware becomes faster, making large-scale password guessing more expensive. |
| Administrator | A user role with elevated permissions, such as managing users, viewing administrative data, or changing application settings. |
| Authentication | The process of verifying a user’s identity, usually with credentials such as an email address and password. |
| Authorization | The process of deciding whether an authenticated user is allowed to perform a particular action or access a particular resource. |
| bcrypt | A widely used adaptive password-hashing algorithm designed to make password guessing computationally expensive. |
| Broken Access Control | A security weakness in which an application does not correctly enforce what an authenticated or unauthenticated user is permitted to access or do. |
| Burp Suite | A web-application security testing platform used to intercept, inspect, modify, and replay HTTP requests and responses. |
| Burp Intruder | A Burp Suite feature used to automate controlled testing of request inputs, such as evaluating how a login endpoint responds to a limited list of password guesses. |
| Burp Proxy | A Burp Suite component that sits between a browser and a web application so that HTTP requests and responses can be inspected. |
| Burp Repeater | A Burp Suite feature that allows a tester to resend and modify an individual HTTP request, then inspect the server’s response. |
| Client-Side Check | A restriction implemented in the browser, such as hiding a link or disabling a button. Client-side checks are not sufficient security controls because a user can alter or send requests directly. |
| Cookie | A small piece of data stored by a web browser and sent with later requests to the same website. Applications commonly use cookies to maintain login sessions. |
| Cross-Site Request Forgery (CSRF) | An attack in which a victim’s browser is induced to submit an unwanted authenticated request to a website where the victim is already logged in. CSRF protections are important for requests that create, modify, or delete data. |
| Cross-Site Scripting (XSS) | A vulnerability that allows attacker-controlled script or markup to run in another user’s browser in the context of a trusted website. |
| Deny by Default | An authorization design principle in which access is refused unless the application explicitly grants permission. |
| Encryption | A reversible process for protecting data so that it can later be decrypted with the appropriate key. Encryption alone is not an appropriate way to store user passwords because passwords should not need to be recovered. |
| Endpoint | A specific application route or URL that receives a request and performs a function, such as a login page, ticket-detail page, or administrator page. |
| Flask | A Python web framework used to build web applications and APIs. |
| Hash | The fixed-length output produced when data is processed through a hashing function. For password storage, the stored hash is used to verify a submitted password without storing the original password in readable form. |
| Horizontal Privilege Escalation | Accessing another user’s resources while remaining at the same permission level. For example, one standard user viewing another standard user’s support ticket. |
| HTTP | Hypertext Transfer Protocol, the protocol used for communication between a browser and a web server. HTTP does not encrypt information in transit. |
| HTTPS | HTTP protected by TLS encryption. HTTPS helps protect credentials, session cookies, and other information while it travels between a browser and a server. |
| HttpOnly | A cookie attribute that prevents client-side JavaScript from directly reading the cookie. It provides an important layer of defense if a cross-site scripting vulnerability exists. |
| IDOR (Insecure Direct Object Reference) | A broken-access-control vulnerability in which an application uses a user-supplied identifier, such as a ticket number, without verifying that the current user is authorized to access the corresponding object. |
| Least Privilege | The principle of granting users, services, and processes only the permissions they need to perform their intended tasks. |
| MD5 | An older, fast hashing function that is not suitable for password storage. Its speed allows attackers to test password guesses very quickly if password-hash data is exposed. |
| OWASP | The Open Worldwide Application Security Project, a nonprofit organization that publishes widely used web-application security guidance, testing resources, and awareness materials. |
| OWASP Top 10 | An OWASP awareness document that identifies major categories of web-application security risk. |
| Parameterized Query | A database-query technique that keeps the query’s instructions separate from supplied input data. It helps prevent SQL injection vulnerabilities. |
| Password Hashing | A one-way process that transforms a password into a stored value. During login, the application hashes the submitted password and compares the result with the stored value; it should not need to recover the original password. |
| PBKDF2 | A password-based key-derivation function that repeats hashing many times to increase the computational cost of password guessing. |
| Plaintext Password | A password stored in readable, unprotected form. Applications should never store user passwords as plaintext. |
| Privilege Escalation | Gaining access to data, functions, or permissions beyond those assigned to the current user. |
| Proof of Concept (PoC) | A controlled demonstration showing that a security issue can be reproduced under the assessment conditions. |
| Role-Based Access Control (RBAC) | An authorization approach that grants permissions based on a user’s assigned role, such as standard user, support agent, or administrator. |
| Salt | A unique, random value combined with a password before hashing. A salt helps ensure that identical passwords do not produce identical stored values and reduces the usefulness of precomputed password-cracking tables. |
| SameSite | A cookie attribute that controls when a browser sends a cookie with cross-site requests. It provides browser-level defense in depth against some CSRF scenarios. |
| Secure Cookie Attribute | A cookie attribute that instructs a browser to send the cookie only over HTTPS connections. |
| Session | A mechanism used by an application to maintain a user’s authenticated state across multiple requests. |
| Session Cookie | A cookie that identifies or helps maintain an authenticated browser session. If it is disclosed to an attacker, it may allow that attacker to impersonate the logged-in user. |
| Session Fixation | An attack in which an attacker attempts to cause a victim to use a session identifier known to the attacker. Regenerating a session identifier after login helps reduce this risk. |
| Session Invalidation | The process of ending a session so that its identifier can no longer be used. A secure logout should invalidate the server-side session or otherwise revoke the associated token. |
| SHA-1 | An older hashing function with known cryptographic weaknesses. Like MD5, it is too fast to use as the sole mechanism for password storage. |
| scrypt | A password-hashing algorithm designed to require substantial memory as well as processing time, increasing the cost of large-scale password guessing. |
| Server-Side Check | A security control enforced by the application server after it receives a request. Server-side authorization checks are required because a user can bypass browser-based restrictions and send requests directly. |
| SQL Injection (SQLi) | A vulnerability that occurs when untrusted input changes the intended meaning of a database query. Successful SQL injection may enable unauthorized data access, modification, or authentication bypass. |
| Standard User | A normal application user without administrative permissions. A standard user should be able to access only the data and functions assigned to that account. |
| TLS | Transport Layer Security, the cryptographic protocol commonly used to secure HTTPS connections. |
| Token | A value used to represent a session, confirm a request, reset a password, or authorize an action. Tokens should be random, protected from disclosure, and limited in lifetime and scope. |
| URL | Uniform Resource Locator, commonly called a web address. In this assessment, ticket identifiers appeared in URLs such as `/tickets/1`. |
| Vertical Privilege Escalation | Accessing functions reserved for a higher-privileged role. For example, a standard user accessing an administrator-only route would be a vertical privilege-escalation issue. |
| Work Factor | A setting that determines how computationally expensive password hashing is. A suitable work factor makes attacker password guesses costly while keeping normal sign-in performance acceptable. |