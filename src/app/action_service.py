import sqlite3
from pathlib import Path

try:
    from .remote_api import call_json
except ImportError:
    from remote_api import call_json

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "database" / "actions.db"


class ActionService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def get_actions(
        category_tag: str | None = None,
        subject: str | None = None,
        id_action: str | None = None,
        observation: str | None = None,
        date_str: str | None = None,
    ):
        status, data = call_json(
            "GET",
            "/actions",
            params={
                "subject": subject,
                "id_action": id_action,
                "observation": observation,
                "date_str": date_str,
            },
        )
        if status == 200 and isinstance(data, list):
            return [
                (
                    row.get("id_action", ""),
                    row.get("matter", ""),
                    row.get("observation", ""),
                    row.get("category", ""),
                    row.get("authorized", ""),
                    row.get("date", ""),
                )
                for row in data
            ]

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT
            id_action,
            matter,
            observation,
            category,
            authorized,
            date
        FROM TABLE_ACTIONS
        WHERE 1 = 1
        """
        params: list[object] = []
        if subject:
            sql += " AND matter LIKE ?"
            params.append(f"%{subject}%")
        if id_action:
            sql += " AND id_action LIKE ?"
            params.append(f"%{id_action}%")
        if observation:
            sql += " AND observation LIKE ?"
            params.append(f"%{observation}%")
        if date_str:
            sql += " AND date = ?"
            params.append(date_str)
        sql += " ORDER BY date DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_action_by_id(id_action: str):
        status, data = call_json("GET", f"/actions/{id_action}")
        if status == 200 and isinstance(data, dict):
            return (
                data.get("id_action", ""),
                data.get("matter", ""),
                data.get("observation", ""),
                data.get("category", ""),
                data.get("solocitated", ""),
                data.get("authorized", ""),
                data.get("date", ""),
                data.get("id_item", ""),
                data.get("descrption", ""),
                data.get("quantity", ""),
                data.get("status", ""),
            )

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id_action,
                matter,
                observation,
                category,
                solocitated,
                authorized,
                date,
                id_item,
                descrption,
                quantity,
                status
            FROM TABLE_ACTIONS
            WHERE id_action = ?
            """,
            (id_action,),
        )
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def get_next_action_id(prefix: str):
        status, data = call_json("GET", f"/actions/next-id/{prefix}")
        if status == 200 and isinstance(data, dict):
            next_id = str(data.get("id_action", ""))
            if next_id.startswith(prefix):
                return next_id

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_action FROM TABLE_ACTIONS WHERE id_action LIKE ? ORDER BY id_action DESC LIMIT 1",
            (f"{prefix}%",),
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return f"{prefix}000001"
        last_id = row[0]
        try:
            num = int(last_id[len(prefix):])
        except ValueError:
            num = 0
        return f"{prefix}{num + 1:06d}"

    @staticmethod
    def insert_action(
        id_action: str,
        matter: str,
        observation: str,
        category: str,
        solocitated: str,
        authorized: str,
        date_str: str,
        id_item: str,
        descrption: str,
        quantity: int | str,
    ):
        status, _ = call_json(
            "POST",
            "/actions",
            payload={
                "id_action": id_action,
                "prefix": id_action[:3],
                "matter": matter,
                "observation": observation,
                "category": category,
                "solocitated": solocitated,
                "authorized": authorized,
                "date_str": date_str,
                "id_item": id_item,
                "descrption": descrption,
                "quantity": str(quantity),
            },
        )
        if status == 201:
            return

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO TABLE_ACTIONS
                (id_action, matter, observation, category, solocitated, authorized, date, id_item, descrption, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_action,
                matter,
                observation,
                category,
                solocitated,
                authorized,
                date_str,
                id_item,
                descrption,
                quantity,
            ),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def list_actions():
        status, data = call_json("GET", "/actions")
        if status == 200 and isinstance(data, list):
            return [
                (
                    row.get("id_action", ""),
                    row.get("matter", ""),
                    row.get("observation", ""),
                    row.get("category", ""),
                    row.get("solocitated", ""),
                    row.get("authorized", ""),
                    row.get("date", ""),
                    row.get("id_item", ""),
                    row.get("descrption", ""),
                    row.get("quantity", ""),
                    row.get("status", ""),
                )
                for row in data
            ]

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id_action,
                matter,
                observation,
                category,
                solocitated,
                authorized,
                date,
                id_item,
                descrption,
                quantity,
                status
            FROM TABLE_ACTIONS
            ORDER BY date DESC
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_action_status(id_action: str, status: str):
        api_status, _ = call_json(
            "PATCH",
            f"/actions/{id_action}/status",
            payload={"status": status},
        )
        if api_status == 200:
            return

        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE TABLE_ACTIONS SET status = ? WHERE id_action = ?",
            (status, id_action),
        )
        conn.commit()
        conn.close()
