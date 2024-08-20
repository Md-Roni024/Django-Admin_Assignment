import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Database configurations from .env file
SOURCE_DB = {
    'dbname': os.getenv('SCRAPY_DATABASE') or 'scrapy_database',
    'user': os.getenv('DB_USER') or 'postgres',
    'password': quote_plus(os.getenv('PASSWORD')) or 'p@stgress',
    'host': os.getenv('HOST') or 'localhost',
    'port': os.getenv('PORT') or '5433'
}

DEST_DB = {
    'dbname': os.getenv('DJANGO_DATABASE') or 'django_database',
    'user': os.getenv('DB_USER') or 'postgres',
    'password': quote_plus(os.getenv('PASSWORD')) or 'p@stgress',
    'host': os.getenv('HOST') or 'localhost',
    'port': os.getenv('PORT') or '5433'
}

IMAGE_PATH = "property_images/"

def confirm_migration():
    """Ask user for confirmation before proceeding with migration."""
    while True:
        confirmation = input("Are you sure you want to migrate data? (Yes/No): ").strip().lower()
        if confirmation in ('yes', 'no'):
            return confirmation == 'yes'
        print("Invalid input. Please enter 'Yes' or 'No'.")

def migrate_data():
    """Perform the data migration from source to destination database."""
    src_conn = None
    src_cursor = None
    dest_conn = None
    dest_cursor = None
    try:
        src_conn = psycopg2.connect(**SOURCE_DB)
        src_cursor = src_conn.cursor()
        dest_conn = psycopg2.connect(**DEST_DB)
        dest_cursor = dest_conn.cursor()

        src_cursor.execute("SELECT id, title, price, room_type, rating, location, latitude, longitude, image_url, image_path FROM hotels_data")
        rows = src_cursor.fetchall()

        for row in rows:
            id, title, price, room_type, rating, location, latitude, longitude, image_url, image_path = row
            current_time = datetime.now()
            dest_cursor.execute("""
                INSERT INTO myapp_property (title, description, price, room_type, rating, create_date, update_date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING property_id;
                """, (title, "NULL", price, room_type, rating, current_time, current_time))

            property_id = dest_cursor.fetchone()[0]
            full_image_path = os.path.join(IMAGE_PATH, os.path.basename(image_path))
            dest_cursor.execute("""
                INSERT INTO myapp_image (image, create_date, property_id, update_date) 
                VALUES (%s, %s, %s, %s)
                """, (full_image_path, current_time, property_id, current_time))
            dest_cursor.execute("""
                SELECT id FROM myapp_location WHERE name = %s AND type = %s AND longitude = %s AND latitude = %s
                """, (location, "", longitude, latitude))
            location_id = dest_cursor.fetchone()

            if not location_id:
                dest_cursor.execute("""
                    INSERT INTO myapp_location (name, type, longitude, latitude, create_date, update_date) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """, (location, "null", longitude, latitude, current_time, current_time))
                location_id = dest_cursor.fetchone()[0]
            else:
                location_id = location_id[0]

            dest_cursor.execute("""
                INSERT INTO myapp_property_locations (property_id, location_id)
                VALUES (%s, %s)
                """, (property_id, location_id))

        dest_conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close all resources if they were successfully opened
        if src_cursor:
            src_cursor.close()
        if src_conn:
            src_conn.close()
        if dest_cursor:
            dest_cursor.close()
        if dest_conn:
            dest_conn.close()

if __name__ == "__main__":
    if confirm_migration():
        migrate_data()
        print("Data successfully migrated.")
    else:
        print("Migration aborted.")
