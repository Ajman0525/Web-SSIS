from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db
from app.user.forms import LoginForm, SignupForm
from app.models.users import UserModel

user_blueprint = Blueprint("user", __name__, template_folder="templates")

# --- LOGIN ---
@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        username = login_form.username.data.strip()
        password = login_form.password.data.strip()

        user = UserModel.get_by_username(username)

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))  # make sure you have this route!
        else:
            login_form.username.errors.append("Incorrect username or password")

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

        existing_users = UserModel.exists(username, email)

        for existing in existing_users:
            if existing[0] == username:
                signup_form.username.errors.append("Username already exists!")
            if existing[1] == email:
                signup_form.email.errors.append("Email already registered!")
    
        if signup_form.errors:
            return render_template("login.html", login_form=login_form, signup_form=signup_form, active_tab="signup")

        success, message = UserModel.create(username, email, password)
        if success:
            flash(message, "success")
            return redirect(url_for("user.login"))
        else:
            flash(message, "danger")

    # GET request or invalid form
    return render_template("login.html", login_form=login_form, signup_form=signup_form)
