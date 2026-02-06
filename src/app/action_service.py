# src/app/action_service.py

import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "database" / "actions.db"   # ajuste se o nome for outro


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
        """
        Retorna ações para a tela de CONSULTAR.

        Tabela (pelo print):
            "id_action"   TEXT PK
            "matter"      REAL NOT NULL      (vou tratar como texto no Python)
            "observation" TEXT
            "category"    TEXT NOT NULL
            "solocitated" TEXT NOT NULL
            "authorized"  TEXT NOT NULL
            "date"        TEXT NOT NULL
            "id_item"     TEXT NOT NULL
            "descreption" TEXT NOT NULL
            "Quantity"    INTEGER NOT NULL
        """

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

        # OBS: por enquanto, o filtro principal é pelo id_action (ACS/ACE).
        # category_tag será usado futuramente quando houver vínculo via id_item.

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
        """
        Busca detalhes completos de uma ação (para abrir depois na tela de Solicitar em modo leitura).
        """

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
        quantity: int,
    ):
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
    def update_action_status(id_action: str, status: str):
        """
        Atualiza o status da ação (CONFIRMADO/CANCELADO).
        """
        conn = ActionService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE TABLE_ACTIONS SET status = ? WHERE id_action = ?",
            (status, id_action),
        )
        conn.commit()
        conn.close()
