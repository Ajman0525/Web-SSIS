from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db
from app.user.forms import LoginForm, SignupForm

user_blueprint = Blueprint("user", __name__, template_folder="templates")

# --- USERS LIST ---
@user_blueprint.route("/users")
def users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT username, email, password_length
        FROM users
        ORDER BY username ASC
    """)
    users_data = cursor.fetchall()
    cursor.close()

    users_list = [
        {"username": u[0], "email": u[1], "password_length": "•" * u[2]}
        for u in users_data
    ]

    return render_template("users.html", page_title="Users", users=users_list)


# --- LOGIN ---
@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        username = login_form.username.data.strip()
        password = login_form.password.data.strip()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))  # make sure you have this route!
        else:
            login_form.username.errors.append("Invalid username or password")

    return render_template("login.html", login_form=login_form, signup_form=signup_form, active_tab="login")


# --- LOGOUT ---
@user_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))


# --- SIGNUP ---
@user_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    login_form = LoginForm()
    signup_form = SignupForm()

    # If form was submitted
    if signup_form.validate_on_submit():
        username = signup_form.username.data.strip()
        email = signup_form.email.data.strip()
        password = signup_form.password.data.strip()

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT username, email FROM users WHERE username=%s OR email=%s",
            (username, email)
        )
        rows = cursor.fetchall()
        for existing in rows:
            if existing[0] == username:
                signup_form.username.errors.append("Username already exists!")
            if existing[1] == email:
                signup_form.email.errors.append("Email already registered!")
    
        if signup_form.errors:
            cursor.close()
            return render_template("login.html", login_form=login_form, signup_form=signup_form, active_tab="signup")

        # Insert new user
        hashed_pw = generate_password_hash(password)
        pw_length = len(password)
        cursor.execute(
            "INSERT INTO users (username, email, password, password_length) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_pw, pw_length)
        )
        db.commit()
        cursor.close()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("user.login"))

    # GET request or invalid form
    return render_template("login.html", login_form=login_form, signup_form=signup_form)
