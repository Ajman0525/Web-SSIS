from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.database import get_db
from app.utils import log_activity
from app.models.programs import ProgramModel
program_blueprint = Blueprint("program", __name__, template_folder="templates")

@program_blueprint.route("/programs")
def programs():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    colleges_list = ProgramModel.get_colleges()

    programs_list = ProgramModel.get_all()

    return render_template(
        "programs.html",
        page_title="Programs",
        programs=programs_list,
        colleges=colleges_list
    )

@program_blueprint.route("/programs/register", methods=["POST"])
def register_program():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()

    # -----REQUIRED FIELDS VALIDATION-----#
    if not code or not name:
        return jsonify(success=False, message="All fields are required."), 400

    db = get_db()
    cursor = db.cursor()
    
    success, message, field = ProgramModel.add(code, name, college_code)
    if success:
        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added new program: {name} ({code}) under college '{college_code}'.",
            url_for('static', filename='add_program.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

@program_blueprint.route("/programs/edit", methods=["POST"])
def edit_program():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()
    original_code = request.form.get("original_code")

    success, message, field = ProgramModel.edit(original_code, code, name, college_code)
    if success:
        #-----RECENTLY EDITED LOGGING-----#
        log_activity(
            f"Updated program: {code} ({name}) under college '{college_code}'.", 
            url_for('static', filename='edit_program.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

@program_blueprint.route("/programs/delete", methods=["POST"])
def delete_program():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return jsonify(success= False, message= "Program code is required to delete."), 400

    success, message = ProgramModel.delete(code)
    if success:
        #-----RECENTLY DLETED LOGGING-----#
        log_activity(
            f"Deleted program: {code}", 
            url_for('static', filename='delete_program.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message), 400
