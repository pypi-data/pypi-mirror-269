import psycopg2
import os

postgre_host = os.getenv("POSTGRE_HOST")
postgre_password = os.getenv("POSTGRE_PASSWORD")
def configure_postgresql():
    # Configure PostgreSQL
    conn = psycopg2.connect(
        host=postgre_host,
        dbname="postgres",
        user="postgres",
        password=postgre_password,
        port=5433
    )
    cursor = conn.cursor()

    # Create a table to store pictures
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pictures (
            id SERIAL PRIMARY KEY,
            cloudinary_id VARCHAR(255),
            cloudinary_url VARCHAR(255)
        )
    """)

    return conn, cursor