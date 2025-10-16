import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.students import StudentModel
from app.database import get_db
from app.utils import log_activity

student_blueprint = Blueprint("student", __name__, template_folder="templates")

@student_blueprint.route("/students")
def students():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    programs_list = StudentModel.get_programs()

    students_list = StudentModel.get_all()

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

    # -----REQUIRED FIELDS VALIDATION-----#
    if not student_id or not first_name or not last_name or not program or not year_level or not gender:
        return jsonify(success= False, message= "All fields are required."), 400
    
    # ---- STUDENT ID VALIDATOR ---- #
    if not re.match(r"^\d{4}-(?!0000)\d{4}$", student_id):
        return jsonify(success= False, message= "Student ID must follow the format."), 400
    
    success, message, field = StudentModel.add(student_id, first_name, last_name, program, year_level, gender)
    if success:    
        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added student {first_name} {last_name} ({student_id}) in {program}.",
            url_for('static', filename='add_student.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

@student_blueprint.route("/students/edit", methods=["POST"])
def edit_student():
    student_id = request.form.get("id", "").strip()
    first_name = request.form.get("f_name", "").strip().title()
    last_name = request.form.get("l_name", "").strip().title()
    program = request.form.get("program", "").strip().title().upper()
    year_level = request.form.get("year_level", "").strip()
    gender = request.form.get("gender", "").strip().title()
    original_id = request.form.get("original_id")

    # ---- STUDENT ID VALIDATOR ---- #
    if not re.match(r"^\d{4}-(?!0000)\d{4}$", student_id):
        return jsonify(success= False, message= "Student ID must follow the format."), 400

    result, message, field = StudentModel.edit(original_id, student_id, first_name, last_name, program, year_level, gender)
    if result == "no_change":
        return jsonify(no_change = True), 200
    
    elif result is True:
        #-----RECENTLY EDITED LOGGING-----#
        log_activity(
            f"Updated student record for {first_name} {last_name} ({student_id}).", 
            url_for('static', filename='edit_student.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

@student_blueprint.route("/students/delete", methods=["POST"])
def delete_student():
    student_id = request.form.get("id", "").strip()

    if not student_id:
        return jsonify(success= False, message= "Student ID is required to delete."), 400

    success, message = StudentModel.delete(student_id)
    if success:
        #-----RECENTLY DELETED LOGGING-----#
        log_activity(
            f"Deleted student record ({student_id}).", 
            url_for('static', filename='delete_student.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message), 400
