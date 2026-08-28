# Spec: Login and Logout

## Overview
Step 3 implements session-based login and logout for Spendly. The `GET /login` route already renders `login.html` with a form, but there is no POST handling, session management, or credential verification. The `GET /logout` route is a placeholder returning a string. This step adds POST handling to `/login` to verify credentials and start a session, replaces the `/logout` placeholder with actual session clearing, and adds a `get_user_by_email()` DB helper. The navbar will also be updated to show the logged-in user's name and a logout link when a session is active.

## Depends on
Step 2 (Registration) must be complete. The `users` table already has `email` and `password_hash` columns, and `werkzeug.security.check_password_hash` is available.

## Routes
- `POST /login` — verify credentials, start session, redirect to profile — public
- `GET /logout` — clear session, redirect to landing — logged-in

## Database changes
No database changes. The `users` table already has the required schema.

## Templates
- **Create:** None
- **Modify:** `templates/login.html` — add per-field error display, preserve email on failure, use `url_for()` for form action
- **Modify:** `templates/base.html` — show user name + logout link when logged in, show sign in + get started when logged out

## Files to change
- `app.py` — add `app.secret_key`, expand `/login` to handle POST, replace `/logout` placeholder, pass `user_id` from session to templates via `@app.context_processor`
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — add per-field error display, preserve email on failure
- `templates/base.html` — conditional navbar for logged-in vs logged-out users

## Files to create
None

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via the existing werkzeug import.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flask.session` for session management (requires `app.secret_key`)
- Session stores `user_id` only — never store password or sensitive data
- `@app.context_processor` injects `user` dict into all templates for navbar rendering
- On login failure, re-render form with email preserved and inline error
- On logout, clear entire session and redirect to landing page
- Update navbar: logged-in shows user name link to `/profile` + logout link; logged-out shows sign in + get started

## Definition of done
- [ ] `POST /login` with valid credentials redirects to `/profile`
- [ ] `POST /login` with wrong password shows "Invalid email or password"
- [ ] `POST /login` with non-existent email shows "Invalid email or password"
- [ ] `POST /login` with missing email shows "Email is required"
- [ ] `POST /login` with missing password shows "Password is required"
- [ ] Login form preserves email address on validation failure
- [ ] `GET /logout` clears session and redirects to landing page
- [ ] Navbar shows user name + logout link when logged in
- [ ] Navbar shows sign in + get started when logged out
- [ ] `session['user_id']` is set after successful login and cleared after logout
