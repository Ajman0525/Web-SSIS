from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db

student_blueprint = Blueprint("student", __name__, template_folder="templates")

@student_blueprint.route("/students")
def students():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
                   SELECT 
                        code,
                        name,
                        college_code
                   FROM programs 
                   ORDER BY code ASC
                   """)
    programs_data = cursor.fetchall()
    cursor.close()

    programs_list = [{"code": p[0], "name": p[1], "college_code": p[2] } for p in programs_data]

    cursor = db.cursor()
    cursor.execute("""
                   SELECT 
                        id,
                        f_name,
                        l_name,
                        program,
                        year_level,
                        gender
                   FROM students 
                   ORDER BY id ASC
                   """)
    students_data = cursor.fetchall()
    cursor.close()

    students_list = [{"id": s[0], 
                      "f_name": s[1], 
                      "l_name": s[2], 
                      "program": s[3], 
                      "year_level": s[4], 
                      "gender": s[5]} 
                    for s in students_data]

    return render_template(
        "students.html",
        page_title="Students",
        students=students_list,
        programs=programs_list
    )

@student_blueprint.route("/students/register", methods=["POST"])
def register_student():
    student_id = request.form.get("id", "").strip()
    first_name = request.form.get("f_name", "").strip().title()
    last_name = request.form.get("l_name", "").strip().title()
    program = request.form.get("program", "").strip().title().upper()
    year_level = request.form.get("year_level", "").strip()
    gender = request.form.get("gender", "").strip().title()

    if not student_id or not first_name or not last_name or not program or not year_level or not gender:
        return {"success": False, "message": "All fields are required."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (id, f_name, l_name, program, year_level, gender) VALUES (%s, %s, %s, %s, %s, %s)", 
            (student_id, first_name, last_name, program, year_level, gender)
        )
        db.commit()
        cursor.close()
        return {"success": True, "message": "Student registered successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

@student_blueprint.route("/students/edit", methods=["POST"])
def edit_student():
    student_id = request.form.get("id", "").strip()
    first_name = request.form.get("f_name", "").strip().title()
    last_name = request.form.get("l_name", "").strip().title()
    program = request.form.get("program", "").strip().title().upper()
    year_level = request.form.get("year_level", "").strip()
    gender = request.form.get("gender", "").strip().title()
    original_id = request.form.get("original_id")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE students SET id = %s, f_name = %s, l_name = %s, program = %s, year_level = %s, gender = %s WHERE id = %s",
            (student_id, first_name, last_name, program, year_level, gender, original_id),
        )
        db.commit()
        cursor.close()
        return {"success": True, "message": "Student updated successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

@student_blueprint.route("/students/delete", methods=["POST"])
def delete_student():
    student_id = request.form.get("id", "").strip()

    if not student_id:
        return {"success": False, "message": "Student ID is required to delete."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        db.commit()
        cursor.close()
        return {"success": True, "message": "Student deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500
