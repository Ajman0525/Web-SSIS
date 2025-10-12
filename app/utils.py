from app.database import get_db

def log_activity(message, icon="bi-info-circle"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO activity_logs (message, icon, timestamp) VALUES (%s, %s, NOW())",
        (message, icon)
    )
    db.commit()
    cursor.close()
