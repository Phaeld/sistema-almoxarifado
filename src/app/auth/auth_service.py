import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

DB_PATH = os.path.join(BASE_DIR, "database", "users.db")
class AuthService:

    @staticmethod
    def authenticate(username, password):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, name, position, level, image_profile, tag
            FROM TABLE_USERS
            WHERE username = ? AND password = ?
        """, (username, password))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "username": row[0],
                "name": row[1],
                "position": row[2],
                "level": row[3],
                "photo": row[4],
                "tag": row[5]
            }

        return None

    @staticmethod
    def update_user_image(username, image_bytes):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE TABLE_USERS SET image_profile = ? WHERE username = ?",
            (image_bytes, username),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def username_exists(username):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM TABLE_USERS WHERE username = ?",
            (username,),
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    @staticmethod
    def create_user(username, name, password, position, level, tag):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO TABLE_USERS (username, name, password, position, level, tag)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, name, password, position, level, tag),
        )
        conn.commit()
        conn.close()
