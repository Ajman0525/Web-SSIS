from flask import Blueprint, render_template, redirect, url_for, session
from app.database import get_db

home_blueprint = Blueprint("home", __name__, template_folder="templates")

@home_blueprint.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    db = get_db()
    cursor = db.cursor()

    # ----- STUDENTS ----- #
    cursor.execute("SELECT COUNT(*) FROM students WHERE program IS NOT NULL")
    enrolled_students = cursor.fetchone()[0] 

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    student_percentage = (
        round((enrolled_students / total_students) * 100, 1)
        if total_students > 0 else 0
    )
    # ----- PROGRAMS ----- #
    cursor.execute("SELECT COUNT(*) FROM programs WHERE college_code IS NOT NULL")
    active_programs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM programs")
    total_programs = cursor.fetchone()[0]

    program_percentage = (
        round((active_programs / total_programs) * 100, 1)
        if total_programs > 0 else 0
    )

    # ----- COLLEGES ----- #
    cursor.execute("SELECT COUNT(*) FROM colleges")
    total_colleges = cursor.fetchone()[0]
    
    cursor.execute("""
                        SELECT COUNT(DISTINCT c.code)
                        FROM colleges c
                        JOIN programs p ON p.college_code = c.code
                    """)
    active_colleges = cursor.fetchone()[0]

    college_percentage = (
        round((active_colleges / total_colleges) * 100, 1)
        if total_colleges > 0 else 0
    )

    user_name = session.get("username")
    return render_template(
        "home.html",
        user_name=user_name,
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges,
        student_percentage=student_percentage,
        program_percentage=program_percentage,
        college_percentage=college_percentage
    )
