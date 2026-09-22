# Evidence Index

This document maps report figures to their source images in the `evidence/` directory.

## A.1 Reconnaissance and Scope

- **Figure 1 – Burp proxy listener configuration**  
  `evidence/01_recon/0-1_proxy_listener.jpg`

- **Figure 2 – Defined target scope in Burp**  
  `evidence/01_recon/0-1_target_scope.jpg`

- **Figure 3 – Burp site map**  
  `evidence/01_recon/1_site_map.jpg`

## A.2 Authentication Testing

- **Figure 4 – Successful login request and response**  
  `evidence/02_authentication/2-1_repeater_with_correct_username_password.jpg`

- **Figure 5 – Login attempt with a non-existent email address**  
  `evidence/02_authentication/2-1_repeater_with_nonexistant_email.jpg`

- **Figure 6 – Login attempt with an incorrect password**  
  `evidence/02_authentication/2-1_repeater_with_wrong_password.jpg`

- **Figure 7 – Intruder payload configuration**  
  `evidence/02_authentication/2-2_intruder_brute-force_setup.jpg`

- **Figure 8 – Intruder results table**  
  `evidence/02_authentication/2-2_intruder_results_table.jpg`

## A.3 Session Management Testing

- **Figure 9 – Set-Cookie header**  
  `evidence/03_session_management/3-1_inspect_set_cookie_header.jpg`

- **Figure 10a – Custom session cookie request**  
  `evidence/03_session_management/3-2_repeater_request_response_custom_cookie.jpg`

- **Figure 10b – Rejection of invalid/tampered session cookie**  
  `evidence/03_session_management/3-2_repeater_request_response_custom_cookie_rejection.jpg`

- **Figure 10c – Post-logout behavior**  
  `evidence/03_session_management/3-3_logout_and_session_invalidation.jpg`

## A.4 Authorization and Access Control Testing

- **Figure 11a – Alice logged in and viewing her ticket (/tickets/1)**  
  `evidence/04_authorization/4-1_ticket1_alice_logged_in.jpg`

- **Figure 11b – Alice’s ticket list (baseline view)**  
  `evidence/04_authorization/4-1_horizontal_privilege_Alice_tickets_1.jpg`

- **Figure 12 – Access to another user’s ticket (/tickets/2)**  
  `evidence/04_authorization/4-1_horizontal_privilege_Alice_tickets_2.jpg`

- **Figure 13 – Repeater view confirming IDOR**  
  `evidence/04_authorization/4-1_IDOR_confirmed_in_repeater_with_response_render.jpg`  
  
- **Figure 14 – SQLite users table**  
  `evidence/04_authorization/4-1_IDOR_list-of-users_sqlite.jpg`