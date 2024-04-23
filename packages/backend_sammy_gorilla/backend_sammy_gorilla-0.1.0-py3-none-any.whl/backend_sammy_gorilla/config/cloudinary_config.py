import cloudinary
from cloudinary import CloudinaryImage
import os

def configure_cloudinary():
    # Configure Cloudinary
    cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"), 
    api_key = os.getenv("CLOUD_API_KEY"), 
    api_secret = os.getenv("CLOUD_API_SECRET")
    )

def fetch_store_pictures(cursor):
    # Fetch pictures from Cloudinary
    cloudinary_pictures = CloudinaryImage().search(expression="type:upload").execute()

    # Store pictures in PostgreSQL
    for pic in cloudinary_pictures['resources']:
        cursor.execute("""
            INSERT INTO pictures (cloudinary_id, cloudinary_url)
            VALUES (%s, %s)
        """, (pic['public_id'], pic['secure_url']))
    conn.commit()

def retrieve_pictures(cursor):
    # Retrieve pictures from PostgreSQL
    cursor.execute("SELECT * FROM pictures")
    pictures_from_db = cursor.fetchall()

    return [{'id': pic[0], 'cloudinary_id': pic[1], 'cloudinary_url': pic[2]} for pic in pictures_from_db]