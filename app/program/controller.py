from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.database import get_db
from app.utils import log_activity

program_blueprint = Blueprint("program", __name__, template_folder="templates")

@program_blueprint.route("/programs")
def programs():
    if "user_id" not in session:
        return redirect(url_for("user.login"))
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
                   SELECT 
                        code,
                        name
                   FROM colleges 
                   ORDER BY code ASC
                   """)
    colleges_data = cursor.fetchall()
    cursor.close()

    colleges_list = [{"code": c[0], "name": c[1]} for c in colleges_data]

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

    if not code or not name:
        return {"success": False, "message": "All fields are required."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO programs (code, name, college_code) VALUES (%s, %s, %s)", 
            (code, name, college_code)
        )
        db.commit()
        cursor.close()

        #-----RECENTLY ADDED LOGGING-----#
        log_activity(
            f"Added new program: {name} ({code}) under college '{college_code}'.",
            url_for('static', filename='add_program.svg')
        )

        return {"success": True, "message": "Program registered successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

@program_blueprint.route("/programs/edit", methods=["POST"])
def edit_program():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()
    original_code = request.form.get("original_code")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE programs SET code = %s, name = %s, college_code = %s WHERE code = %s",
            (code, name, college_code, original_code),
        )
        db.commit()
        cursor.close()

        #-----RECENTLY EDITED LOGGING-----#
        log_activity(
            f"Updated program: {code} ({name}) under college '{college_code}'.", 
            url_for('static', filename='edit_program.svg')
        )

        return {"success": True, "message": "Program updated successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

@program_blueprint.route("/programs/delete", methods=["POST"])
def delete_program():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return {"success": False, "message": "Program code is required to delete."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT name FROM programs WHERE code = %s", (code,))
        row = cursor.fetchone()
        name = row[0] if row else code

        cursor.execute("DELETE FROM programs WHERE code = %s", (code,))
        db.commit()
        cursor.close()

        #-----RECENTLY DLETED LOGGING-----#
        log_activity(
            f"Deleted program: {name} ({code})", 
            url_for('static', filename='delete_program.svg')
        )

        return {"success": True, "message": "Program deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500
