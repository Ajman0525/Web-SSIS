from app.database import get_db

class ProgramModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY code ASC")
        programs_data = cursor.fetchall()
        cursor.close()
        return [{"code": p[0], "name": p[1], "college_code": p[2]} for p in programs_data]
    
    @staticmethod
    def get_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT code, name FROM colleges ORDER BY code ASC")
        colleges_data = cursor.fetchall()
        cursor.close()
        return [{"code": c[0], "name": c[1]} for c in colleges_data]
    
    @staticmethod
    def exists_by_code(code):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM programs WHERE code = %s", (code,))
        (count,) = cursor.fetchone()
        cursor.close()
        return count > 0
    
    @staticmethod
    def exists_by_name(name):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM programs WHERE name = %s", (name,))
        (count,) = cursor.fetchone()
        cursor.close()
        return count > 0
    
    @staticmethod
    def add(code, name, college_code):
        if ProgramModel.exists_by_code(code):
            return False, "Program code already exists. Please use a different code.", "code"
        if ProgramModel.exists_by_name(name):
            return False, "Program name already exists. Please use a different name.", "name"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO programs (code, name, college_code) VALUES (%s, %s, %s)",
                (code, name, college_code),
            )
            db.commit()
            cursor.close()
            return True, f"Program {name} ({code}) added successfully!", None
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e), None
        
    @staticmethod
    def edit(original_code, code, name, college_code):
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT name FROM programs WHERE code = %s", (original_code,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return False, "College not found.", None

        original_name = row[0] 

        if code != original_code and ProgramModel.exists_by_code(code):
            cursor.close()
            return False, "Program code already exists. Please use a different code.", "code"
        
        if name != original_name and ProgramModel.exists_by_name(name):
            cursor.close()
            return False, "Program name already exists. Please use a different name.", "name"
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                UPDATE programs 
                SET code = %s, name = %s, college_code = %s 
                WHERE code = %s
                """,
                (code, name, college_code, original_code),
            )
            db.commit()
            cursor.close()
            return True, f"Program updated successfully!", None
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e), None
        
    @staticmethod
    def delete(code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT name FROM programs WHERE code = %s", (code,))
            row = cursor.fetchone()
            name = row[0] if row else code

            cursor.execute("DELETE FROM programs WHERE code = %s", (code,))
            db.commit()
            cursor.close()
            return True, f"Deleted program: {name} ({code})"
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e)