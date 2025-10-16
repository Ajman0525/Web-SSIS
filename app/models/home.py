from app.database import get_db
from datetime import datetime

class HomeModel:
    @staticmethod
    def get_student_counts():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE program IS NOT NULL")
        enrolled_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        cursor.close()
        return enrolled_students, total_students

    @staticmethod
    def get_program_counts():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM programs WHERE college_code IS NOT NULL")
        active_programs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM programs")
        total_programs = cursor.fetchone()[0]
        cursor.close()
        return active_programs, total_programs

    @staticmethod
    def get_college_counts():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM colleges")
        total_colleges = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT c.code)
            FROM colleges c
            JOIN programs p ON p.college_code = c.code
        """)
        active_colleges = cursor.fetchone()[0]
        cursor.close()
        return active_colleges, total_colleges

    @staticmethod
    def get_recent_activities(limit=5):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT message, icon, timestamp
            FROM activity_logs
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        rows = cursor.fetchall()
        cursor.close()

        activities = []
        for message, icon, ts in rows:
            diff = (datetime.now() - ts).total_seconds()
            if diff < 3600:
                time_ago = f"{int(diff // 60)}m ago"
            elif diff < 86400:
                time_ago = f"{int(diff // 3600)}h ago"
            else:
                time_ago = f"{int(diff // 86400)}d ago"

            activities.append({"message": message, "icon": icon, "timestamp": ts, "time_ago": time_ago})
        return activities