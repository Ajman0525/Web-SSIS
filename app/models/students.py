from app.database import get_db


class StudentModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id ASC")
        students_data = cursor.fetchall()
        cursor.close()
        return [{   "id": s[0], 
                    "f_name": s[1], 
                    "l_name": s[2], 
                    "program": s[3], 
                    "year_level": s[4], 
                    "gender": s[5]} 
                for s in students_data]
    
    @staticmethod
    def get_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT code, name, college_code FROM programs ORDER BY code ASC")
        programs_data = cursor.fetchall()
        cursor.close()
        return [{"code": p[0], "name": p[1], "college_code": p[2] } for p in programs_data]
    
    @staticmethod
    def exists_by_id(student_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE id = %s", (student_id,))
        (count,) = cursor.fetchone()
        cursor.close()
        return count > 0
    
    @staticmethod
    def add(student_id, first_name, last_name, program, year_level, gender):
        if StudentModel.exists_by_id(student_id):
            return False, "Student ID already exists. Please use a different ID.", "id"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (id, f_name, l_name, program, year_level, gender) VALUES (%s, %s, %s, %s, %s, %s)", 
                (student_id, first_name, last_name, program, year_level, gender)
            )
            db.commit()
            cursor.close()
            return True, f"Student {first_name} {last_name} ({student_id}) added successfully!", None
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e), None 
        
    @staticmethod
    def edit(original_id, student_id, first_name, last_name, program, year_level, gender):
        if student_id != original_id and StudentModel.exists_by_id(student_id):
            return False, "Student ID already exists. Please use a different ID.", "student_id"
        

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE students SET id = %s, f_name = %s, l_name = %s, program = %s, year_level = %s, gender = %s WHERE id = %s",
                (student_id, first_name, last_name, program, year_level, gender, original_id),
            )
            db.commit()
            cursor.close()
            return True, f"Student {first_name} {last_name} ({student_id}) updated successfully!", None
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e), None
        
    @staticmethod
    def delete(student_id):       
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT f_name, l_name FROM students WHERE id = %s", (student_id,))
            row = cursor.fetchone()
            student_name = f"{row[0]} {row[1]}" if row else student_id

            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            db.commit()
            cursor.close()
            return True, f"Deleted student record: {student_name} ({student_id})"
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e)