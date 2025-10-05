from flask import Blueprint, render_template, redirect, url_for, session
from app.database import get_db

home_blueprint = Blueprint("home", __name__, template_folder="templates")

@home_blueprint.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM programs")
    total_programs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM colleges")
    total_colleges = cursor.fetchone()[0]

    user_name = session.get("username")
    return render_template(
        "home.html",
        user_name=user_name,
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges
    )
