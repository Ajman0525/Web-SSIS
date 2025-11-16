from supabase import create_client, Client
from flask import current_app
import os
from werkzeug.utils import secure_filename
import uuid
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

def get_supabase_client() -> Client:
    supabase_url = current_app.config['SUPABASE_URL']
    supabase_key = current_app.config['SUPABASE_SERVICE_KEY']
    return create_client(supabase_url, supabase_key)

def upload_student_photo(file, student_id):
    if not file:
        return None
    
    try:
        # Get file extension
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        
        # Create unique filename: studentid_uuid.ext
        unique_filename = f"{student_id}_{uuid.uuid4().hex[:8]}{file_ext}"
        
        # Read file data
        file_data = file.read()
        
        # Get Supabase client
        supabase = get_supabase_client()
        bucket_name = current_app.config['SUPABASE_BUCKET_NAME']
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(bucket_name).upload(
            path=unique_filename,
            file=file_data,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading photo: {str(e)}")
        return None

def delete_student_photo(photo_url):
    if not photo_url:
        return True
    
    try:
        # Extract filename from URL
        filename = photo_url.split('/')[-1]
        
        # Get Supabase client
        supabase = get_supabase_client()
        bucket_name = current_app.config['SUPABASE_BUCKET_NAME']
        
        # Delete from Supabase Storage
        supabase.storage.from_(bucket_name).remove([filename])
        
        return True
        
    except Exception as e:
        print(f"Error deleting photo: {str(e)}")
        return False

def update_student_photo(file, student_id, old_photo_url=None):
    # Delete old photo if exists
    if old_photo_url:
        delete_student_photo(old_photo_url)
    
    # Upload new photo
    return upload_student_photo(file, student_id)
