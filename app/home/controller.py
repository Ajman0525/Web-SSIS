# from flask import Blueprint, render_template, redirect, url_for, session

# home_blueprint = Blueprint("home", __name__, template_folder="templates")

# @home_blueprint.route("/")
# def home():
#     if "user_id" not in session:
#         return redirect(url_for("user.login"))

#     # Debug: see session content in console
#     print("SESSION CONTENT:", dict(session))

#     user_name = session.get("username")
#     if not user_name:
#         return "Session username not found", 500

#     return render_template("home.html", user_name=user_name)
