# Spec: Registration

## Overview
Step 2 implements the full registration flow for Spendly. The `GET /register` route already exists and renders `register.html`, but there is no form handling, validation, or user creation logic. This step adds POST handling to the register route, validates form input, hashes the password, inserts the new user into the database, and redirects to the login page on success or re-renders the form with errors on failure.

## Depends on
Step 1 (Landing page) must be complete. The `users` table already exists in `database/db.py` with columns `id`, `name`, `email`, `password_hash`, and `created_at`.

## Routes
- `POST /register` — process registration form, create user, redirect to login — public

## Database changes
No database changes. The `users` table already has the required schema.

## Templates
- **Create:** None
- **Modify:** `templates/register.html` — add a `<form>` with fields for name, email, password, and confirm password; submit button; display validation errors

## Files to change
- `app.py` — add POST method to `/register` route, call helper in `database/db.py`
- `database/db.py` — add `create_user(name, email, password)` helper function
- `templates/register.html` — build out the registration form

## Files to create
None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders)
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validation errors displayed inline next to each field
- On success, redirect to `/login` with a success flash message or query param
- On failure, re-render form with previous values preserved (except password)
- Email uniqueness check: if email already exists, show "Email already registered"
- Name required, email required + valid format, password required + min 6 chars, confirm password must match

## Definition of done
- [ ] `POST /register` with valid data creates a user in the database and redirects to `/login`
- [ ] `POST /register` with missing name shows "Name is required"
- [ ] `POST /register` with missing email shows "Email is required"
- [ ] `POST /register` with invalid email format shows "Invalid email address"
- [ ] `POST /register` with short password (< 6 chars) shows "Password must be at least 6 characters"
- [ ] `POST /register` with mismatched passwords shows "Passwords do not match"
- [ ] `POST /register` with existing email shows "Email already registered"
- [ ] Registration form preserves previously entered values on validation failure
- [ ] New user appears in the `users` table with a hashed password
