# model/db.py
import mysql.connector

db_config = {
    "host": "152.42.234.69",
    "user": "reqease",
    "password": "reqease2024uic",
    "database": "reqEase",
    "port": 3306,
}

def get_db():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        yield cursor, db
    finally:
        cursor.close()
        db.close()
        