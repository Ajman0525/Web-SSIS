import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.students import StudentModel
from app.database import get_db
from app.utils import log_activity, upload_student_photo, delete_student_photo, update_student_photo

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
    program = request.form.get("program", "").strip().upper()
    year_level = request.form.get("year_level", "").strip()
    gender = request.form.get("gender", "").strip().title()
    
    # Get photo file
    photo_file = request.files.get('photo')

    # -----REQUIRED FIELDS VALIDATION-----#
    if not student_id or not first_name or not last_name or not program or not year_level or not gender:
        return jsonify(success=False, message="All fields are required."), 400
    
    # ---- STUDENT ID VALIDATOR ---- #
    if not re.match(r"^\d{4}-(?!0000)\d{4}$", student_id):
        return jsonify(success=False, message="Student ID must follow the format."), 400
    
    # Upload photo to Supabase if provided
    photo_url = None
    if photo_file and photo_file.filename:
        photo_url = upload_student_photo(photo_file, student_id)
        if photo_url is None and photo_file.filename:
            return jsonify(success=False, message="Failed to upload photo. Please check file type and size."), 400
    
    success, message, field = StudentModel.add(student_id, first_name, last_name, program, year_level, gender, photo_url)
    
    if success:    
        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added student {first_name} {last_name} ({student_id}) in {program}.",
            url_for('static', filename='add_student.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        # If database save fails, delete uploaded photo
        if photo_url:
            delete_student_photo(photo_url)
        return jsonify(success=False, message=message, field=field), 400

@student_blueprint.route("/students/edit", methods=["POST"])
def edit_student():
    original_id = request.form.get("original_id", "").strip()
    student_id = request.form.get("id", "").strip()
    first_name = request.form.get("f_name", "").strip().title()
    last_name = request.form.get("l_name", "").strip().title()
    program = request.form.get("program", "").strip().upper()
    year_level = request.form.get("year_level", "").strip()
    gender = request.form.get("gender", "").strip().title()
    
    current_photo = request.form.get('current_photo', '').strip()
    remove_photo = request.form.get('remove_photo') == 'true'
    photo_file = request.files.get('photo')

    # ---- STUDENT ID VALIDATOR ---- #
    if not re.match(r"^\d{4}-(?!0000)\d{4}$", student_id):
        return jsonify(success=False, message="Student ID must follow the format."), 400

    # Handle photo logic
    photo_url = current_photo if current_photo else None
    
    if remove_photo:
        # Remove photo
        if current_photo:
            delete_student_photo(current_photo)
        photo_url = None
        
    elif photo_file and photo_file.filename:
        # Upload new photo
        new_photo_url = update_student_photo(photo_file, student_id, current_photo)
        if new_photo_url:
            photo_url = new_photo_url
        else:
            return jsonify(success=False, message="Failed to upload photo. Please check file type and size."), 400

    result, message, field = StudentModel.edit(original_id, student_id, first_name, last_name, program, year_level, gender, photo_url)
    
    if result == "no_change":
        return jsonify(no_change=True), 200
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
        return jsonify(success=False, message="Student ID is required to delete."), 400

    success, message, student_photo = StudentModel.delete(student_id)
    
    if success:
        # Delete photo from Supabase if exists
        if student_photo:
            delete_student_photo(student_photo)
            
        #-----RECENTLY DELETED LOGGING-----#
        log_activity(
            f"Deleted student record ({student_id}).", 
            url_for('static', filename='delete_student.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message), 400