import sqlite3
import os
import base64
try:
    from ..remote_api import call_json
except ImportError:
    from remote_api import call_json

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
        status, data = call_json(
            "POST",
            "/auth/login",
            payload={"username": username, "password": password},
        )
        if status == 200 and isinstance(data, dict):
            photo = data.get("photo")
            if isinstance(photo, str):
                try:
                    photo = base64.b64decode(photo)
                except Exception:
                    photo = None
            return {
                "username": data.get("username", ""),
                "name": data.get("name", ""),
                "position": data.get("position", ""),
                "level": data.get("level", 0),
                "photo": photo,
                "tag": data.get("tag"),
            }

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
        encoded = base64.b64encode(image_bytes).decode("ascii") if image_bytes else ""
        status, _ = call_json(
            "PATCH",
            f"/users/{username}/image",
            payload={"image_base64": encoded},
        )
        if status == 200:
            return

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
        status, data = call_json("GET", f"/users/{username}/exists")
        if status == 200 and isinstance(data, dict):
            return bool(data.get("exists"))

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
        status, _ = call_json(
            "POST",
            "/users",
            payload={
                "username": username,
                "name": name,
                "password": password,
                "position": position,
                "level": level,
                "tag": tag,
            },
        )
        if status == 201:
            return

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

    @staticmethod
    def list_users():
        status, data = call_json("GET", "/users")
        if status == 200 and isinstance(data, list):
            return [
                (
                    int(row.get("id_user", 0)),
                    row.get("username", ""),
                    row.get("name", ""),
                    row.get("position", ""),
                    int(row.get("level", 0)),
                    row.get("tag", ""),
                )
                for row in data
            ]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_user, username, name, position, level, tag
            FROM TABLE_USERS
            ORDER BY name
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_user(user_id, username, name, password, position, level, tag):
        status, _ = call_json(
            "PUT",
            f"/users/{user_id}",
            payload={
                "username": username,
                "name": name,
                "password": password,
                "position": position,
                "level": level,
                "tag": tag,
            },
        )
        if status == 200:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE TABLE_USERS
            SET username = ?, name = ?, password = ?, position = ?, level = ?, tag = ?
            WHERE id_user = ?
            """,
            (username, name, password, position, level, tag, user_id),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        status, _ = call_json("DELETE", f"/users/{user_id}")
        if status == 200:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TABLE_USERS WHERE id_user = ?", (user_id,))
        conn.commit()
        conn.close()
