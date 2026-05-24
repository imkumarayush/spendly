# Spendly Project Structure

## Overview

Spendly is a Flask-based personal finance tracker. The project is organized as follows:

```text
.expense-tracker/
├── app.py
├── requirements.txt
├── venv/
├── database/
│   ├── __init__.py
│   └── db.py
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── landing.html
    ├── login.html
    └── register.html
```

## Key Components

- **app.py**: Entry point, defines routes and renders templates.
- **database/db.py**: Handles SQLite operations.
- **templates/**: Jinja2 HTML templates.
- **static/**: CSS and JavaScript assets.
- **requirements.txt**: Python dependencies.
- **venv/**: Virtual environment for isolated Python packages.

Each part plays a specific role in serving the web UI, managing data, and handling user interactions.