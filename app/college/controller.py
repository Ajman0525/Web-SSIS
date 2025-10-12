from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.database import get_db
from app.utils import log_activity

college_blueprint = Blueprint("college", __name__, template_folder="templates")

@college_blueprint.route("/colleges")
def colleges():
    if "user_id" not in session:
        return redirect(url_for("user.login"))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM colleges ORDER BY code ASC")
    colleges_data = cursor.fetchall()
    cursor.close()

    colleges_list = [{"code": c[0], "name": c[1]} for c in colleges_data]

    return render_template(
        "colleges.html",
        page_title="Colleges",
        colleges=colleges_list,
    )

@college_blueprint.route("/colleges/register", methods=["POST"])
def register_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()

    if not code or not name:
        return {"success": False, "message": "All fields are required."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO colleges (code, name) VALUES (%s, %s)", 
            (code, name)
        )
        db.commit()
        cursor.close()

        #-----RECENTLY ADDED LOGGING-----#
        log_activity(f"Added new college: {name} ({code})", "bi-building-add")

        return {"success": True, "message": "College registered successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500

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
        log_activity(f"Updated college '{original_code}' → '{name}' ({code})", "bi-pencil-square")

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
        log_activity(f"Deleted college: {name} ({code})", "bi-trash3")
        
        return {"success": True, "message": "College deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500
