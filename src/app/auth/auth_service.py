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
            SELECT username
            FROM TABLE_USERS
            WHERE username = ? AND password = ?
        """, (username, password))

        user = cursor.fetchone()
        conn.close()

        return user  # None se não existir
