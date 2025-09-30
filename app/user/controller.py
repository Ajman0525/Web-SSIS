from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/users")
def users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
                    SELECT username,
                           email,
                           password
                   FROM users
                   ORDER BY username ASC
                   """)
    users_data = cursor.fetchall()
    cursor.close()

    users_list = [{"username": u[0], "email": u[1], "password": u[2]} for u in users_data]

    return render_template(
        "users.html",
        page_title="Users",
        users=users_list
    )

# --- LOGIN ---
@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):  # user[2] = hashed password
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("home"))  # 👈 this redirects to home.html
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


# --- SIGNUP ---
@user_blueprint.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not email or not password:
        flash("All fields are required!", "danger")
        return redirect(url_for("user.login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        flash("Username already exists!", "danger")
        return redirect(url_for("user.login"))

    hashed_pw = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_pw),
    )
    db.commit()
    cursor.close()

    flash("Account created successfully! Please log in.", "success")
    return redirect(url_for("user.login"))
