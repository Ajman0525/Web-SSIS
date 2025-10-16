from flask import Blueprint, render_template, redirect, url_for, session
from app.models.home import HomeModel

home_blueprint = Blueprint("home", __name__, template_folder="templates")

@home_blueprint.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    enrolled_students, total_students = HomeModel.get_student_counts()
    student_percentage = round((enrolled_students / total_students) * 100, 1) if total_students else 0

    active_programs, total_programs = HomeModel.get_program_counts()
    program_percentage = round((active_programs / total_programs) * 100, 1) if total_programs else 0

    active_colleges, total_colleges = HomeModel.get_college_counts()
    college_percentage = round((active_colleges / total_colleges) * 100, 1) if total_colleges else 0

    recent_activities = HomeModel.get_recent_activities()

    user_name = session.get("username")
    return render_template(
        "home.html",
        user_name=user_name,
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges,
        student_percentage=student_percentage,
        program_percentage=program_percentage,
        college_percentage=college_percentage,
        recent_activities=recent_activities
    )
