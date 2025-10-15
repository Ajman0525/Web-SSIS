# app/models/college_model.py
from app.database import get_db
from flask import jsonify

class CollegeModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM colleges ORDER BY code ASC")
        colleges_data = cursor.fetchall()
        cursor.close()
        return [{"code": c[0], "name": c[1]} for c in colleges_data]

    @staticmethod
    def exists_by_code(code):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM colleges WHERE code = %s", (code,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    @staticmethod
    def exists_by_name(name):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM colleges WHERE name = %s", (name,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    @staticmethod
    def add(code, name):
        if CollegeModel.exists_by_code(code):
            return False, "College code already exists. Please use a different code.", "code"
        if CollegeModel.exists_by_name(name):
             return False, "College name already exists. Please use a different name.", "name"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO colleges (code, name) VALUES (%s, %s)", 
                (code, name)
            )
            db.commit()
            cursor.close()
            return True, "College registered successfully!", None
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e), None

    @staticmethod
    def edit(original_code, code, name):
        # Check for duplicates only if user changed code/name
        if code != original_code and CollegeModel.exists_by_code(code):
            return jsonify(success=False, field="code", message= "College code already exists."), 400
        if CollegeModel.exists_by_name(name):
            return jsonify(success=False, field="name", message="College name already exists."), 400
       
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE colleges SET code = %s, name = %s WHERE code = %s",
                (code, name, original_code),
            )
            db.commit()
            cursor.close()
            return True, "College updated successfully!"
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e)

    @staticmethod
    def delete(code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT name FROM colleges WHERE code = %s", (code,))
            row = cursor.fetchone()
            name = row[0] if row else code

            cursor.execute("DELETE FROM colleges WHERE code = %s", (code,))
            db.commit()
            cursor.close()
            return True, f"Deleted college: {name} ({code})"
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e)
