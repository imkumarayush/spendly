from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Context processor — inject user into all templates                  #
# ------------------------------------------------------------------ #

@app.context_processor
def inject_user():
    user_id = session.get("user_id")
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            return {"user": {"name": user["name"], "email": user["email"]}}
    return {"user": None}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    errors = {}

    if not name:
        errors["name"] = "Name is required"

    if not email:
        errors["email"] = "Email is required"
    elif "@" not in email or "." not in email:
        errors["email"] = "Invalid email address"

    if not password:
        errors["password"] = "Password is required"
    elif len(password) < 6:
        errors["password"] = "Password must be at least 6 characters"

    if password != confirm_password:
        errors["confirm_password"] = "Passwords do not match"

    if errors:
        return render_template("register.html", errors=errors, name=name, email=email)

    if not create_user(name, email, password):
        return render_template("register.html", errors={"email": "Email already registered"}, name=name, email=email)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    errors = {}

    if not email:
        errors["email"] = "Email is required"

    if not password:
        errors["password"] = "Password is required"

    if errors:
        return render_template("login.html", errors=errors, email=email)

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", errors={"general": "Invalid email or password"}, email=email)

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    profile_data = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "joined": "August 2026",
        "stats": {
            "total_spent": "₹358.24",
            "transaction_count": 8,
            "top_category": "Bills",
        },
        "transactions": [
            {"date": "2026-08-18", "description": "Miscellaneous", "category": "Other", "amount": "₹20.00"},
            {"date": "2026-08-15", "description": "Lunch with friends", "category": "Food", "amount": "₹12.75"},
            {"date": "2026-08-12", "description": "New headphones", "category": "Shopping", "amount": "₹89.99"},
            {"date": "2026-08-10", "description": "Movie tickets", "category": "Entertainment", "amount": "₹30.00"},
            {"date": "2026-08-07", "description": "Pharmacy", "category": "Health", "amount": "₹45.00"},
        ],
        "categories": [
            {"name": "Bills", "total": "₹120.00", "percent": 33},
            {"name": "Shopping", "total": "₹89.99", "percent": 25},
            {"name": "Health", "total": "₹45.00", "percent": 13},
            {"name": "Entertainment", "total": "₹30.00", "percent": 8},
            {"name": "Food", "total": "₹38.25", "percent": 11},
        ],
    }

    return render_template("profile.html", profile=profile_data)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
