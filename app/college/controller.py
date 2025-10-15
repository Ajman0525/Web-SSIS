from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.database import get_db
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

    existing_code = CollegeModel.exists_by_code(code)
    existing_name = CollegeModel.exists_by_name(name)
    
    if existing_code:
        return jsonify(success=False, message="College code already exists."), 400
    elif existing_name:
        return jsonify(success=False, message="College name already exists."), 400
    
    success, message = CollegeModel.add(code, name)
    if success:
        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added new college: {name} ({code})", 
            url_for('static', filename='add_college.svg')
        )
        return jsonify(success=True, message=message), 200
    else:
        return jsonify(success=False, message=message), 400

 

@college_blueprint.route("/colleges/edit", methods=["POST"])
def edit_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    original_code = request.form.get("original_code")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE colleges SET code = %s, name = %s WHERE code = %s",
            (code, name, original_code),
        )
        db.commit()
        cursor.close()

        #-----RECENTLY EDITED LOGGING-----#
        log_activity(
            f"Updated college '{original_code}' → '{name}' ({code})", 
            url_for('static', filename='edit_college.svg')
        )

        return {"success": True, "message": "College updated successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

@college_blueprint.route("/colleges/delete", methods=["POST"])
def delete_college():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return {"success": False, "message": "College code is required to delete."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT name FROM colleges WHERE code = %s", (code,))
        row = cursor.fetchone()
        name = row[0] if row else code

        cursor.execute("DELETE FROM colleges WHERE code = %s", (code,))
        db.commit()
        cursor.close()

        #-----RECENTLY DLETED LOGGING-----#
        log_activity(
            f"Deleted college: {name} ({code})", 
            url_for('static', filename='delete_college.svg')
        )
        
        return {"success": True, "message": "College deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500
