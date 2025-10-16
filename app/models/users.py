from app.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT username, email, password_length FROM users ORDER BY username ASC")
        users_data = cursor.fetchall()
        cursor.close()
        return [
            {"username": u[0], "email": u[1], "password_length": "•" * u[2]}
            for u in users_data
        ]

    @staticmethod
    def get_by_username(username):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def exists(username, email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT username, email FROM users WHERE username=%s OR email=%s", (username, email))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @staticmethod
    def create(username, email, password):
        hashed_pw = generate_password_hash(password)
        pw_length = len(password)

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, password_length) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_pw, pw_length)
            )
            db.commit()
            return True, "Account created successfully!"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
