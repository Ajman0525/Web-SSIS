from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.utils import log_activity
from app.models.colleges import CollegeModel
college_blueprint = Blueprint("college", __name__, template_folder="templates")

@college_blueprint.route("/colleges")
def colleges():
    if "user_id" not in session:
        return redirect(url_for("user.login"))

    colleges_list = CollegeModel.get_all()

    return render_template(
        "colleges.html",
        page_title="Colleges",
        colleges=colleges_list,
    )

@college_blueprint.route("/colleges/register", methods=["POST"])
def register_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()

    # -----REQUIRED FIELDS VALIDATION-----#
    if not code or not name:
        return jsonify(success=False, message="All fields are required."), 400

    success, message, field = CollegeModel.add(code, name)
    if success:
        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added new college: {name} ({code})", 
            url_for('static', filename='add_college.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

 

@college_blueprint.route("/colleges/edit", methods=["POST"])
def edit_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    original_code = request.form.get("original_code")

    # -----REQUIRED FIELDS VALIDATION-----#
    if not code or not name:
        return jsonify(success=False, message="All fields are required."), 400
    
    success, message, field = CollegeModel.edit(original_code, code, name)
    if success:
        #-----RECENTLY EDITED LOGGING-----#
        log_activity(
            f"Updated college '{original_code}' → '{name}' ({code})", 
            url_for('static', filename='edit_college.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message, field=field), 400

@college_blueprint.route("/colleges/delete", methods=["POST"])
def delete_college():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return jsonify(success=False, message="College code is required to delete."), 400

    success, message = CollegeModel.delete(code)
    if success:
        #-----RECENTLY DLETED LOGGING-----#
        log_activity(
            f"Deleted college: {code})", 
            url_for('static', filename='delete_college.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message), 400
