"""
====================================================================
    MATERIAL SERVICE
--------------------------------------------------------------------
    Funcoes de acesso a tabela TABLE_MATERIAL do banco material.db
====================================================================
"""

import os
import sqlite3

try:
    from .remote_api import call_json
except ImportError:
    from remote_api import call_json


CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "material.db")


CATEGORY_PREFIX_MAP = {
    "LIM": "L",
    "ELE": "E",
    "HID": "H",
    "FER": "F",
    "AUT": "A",
}


class MaterialService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def get_materials(
        category_tag=None,
        description=None,
        item_number=None,
        product=None,
        category=None,
    ):
        status, data = call_json(
            "GET",
            "/materials",
            params={
                "category_tag": category_tag,
                "description": description,
                "item_number": item_number,
                "product": product,
                "category": category,
            },
        )
        if status == 200 and isinstance(data, list):
            return [
                (
                    row.get("id_item", ""),
                    row.get("descrption", ""),
                    row.get("product", ""),
                    row.get("category", ""),
                    row.get("quantity", 0),
                    row.get("unit_measurement", ""),
                )
                for row in data
            ]

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        query = """
            SELECT
                id_item,
                descreption,
                product,
                category,
                quantity,
                unit_measurement
            FROM TABLE_MATERIAL
            WHERE 1 = 1
        """
        params = []
        if category_tag:
            prefix = CATEGORY_PREFIX_MAP.get(category_tag)
            if prefix:
                query += " AND id_item LIKE ?"
                params.append(f"{prefix}%")
        if description:
            query += " AND descreption LIKE ?"
            params.append(f"%{description}%")
        if item_number:
            query += " AND id_item LIKE ?"
            params.append(f"%{item_number}%")
        if product:
            query += " AND product LIKE ?"
            params.append(f"%{product}%")
        if category:
            query += " AND category LIKE ?"
            params.append(f"%{category}%")
        query += " ORDER BY id_item ASC"
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_material_by_id(id_item):
        status, data = call_json("GET", f"/materials/{id_item}")
        if status == 200 and isinstance(data, dict):
            return (
                data.get("id_item", ""),
                data.get("descrption", ""),
                data.get("product", ""),
                data.get("category", ""),
                data.get("quantity", 0),
                data.get("unit_measurement", ""),
            )

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                id_item,
                descreption,
                product,
                category,
                quantity,
                unit_measurement
            FROM TABLE_MATERIAL
            WHERE id_item = ?
            """,
            (id_item,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def get_distinct_products():
        status, data = call_json("GET", "/materials/distinct/products")
        if status == 200 and isinstance(data, list):
            return [str(item) for item in data]

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT product FROM TABLE_MATERIAL ORDER BY product")
        values = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def get_distinct_categories():
        status, data = call_json("GET", "/materials/distinct/categories")
        if status == 200 and isinstance(data, list):
            return [str(item) for item in data]

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM TABLE_MATERIAL ORDER BY category")
        values = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def create_material(
        id_item,
        descrption,
        product,
        category,
        quantity,
        unit_measurement,
    ):
        status, _ = call_json(
            "POST",
            "/materials",
            payload={
                "id_item": id_item,
                "descrption": descrption,
                "product": product,
                "category": category,
                "quantity": quantity,
                "unit_measurement": unit_measurement,
            },
        )
        if status == 201:
            return

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO TABLE_MATERIAL
                (id_item, descreption, product, category, quantity, unit_measurement)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id_item, descrption, product, category, quantity, unit_measurement),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update_material(
        id_item,
        descrption,
        product,
        category,
        quantity,
        unit_measurement,
    ):
        status, _ = call_json(
            "PUT",
            f"/materials/{id_item}",
            payload={
                "descrption": descrption,
                "product": product,
                "category": category,
                "quantity": quantity,
                "unit_measurement": unit_measurement,
            },
        )
        if status == 200:
            return

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE TABLE_MATERIAL
            SET descreption = ?, product = ?, category = ?, quantity = ?, unit_measurement = ?
            WHERE id_item = ?
            """,
            (descrption, product, category, quantity, unit_measurement, id_item),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_material(id_item):
        status, _ = call_json("DELETE", f"/materials/{id_item}")
        if status == 200:
            return

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TABLE_MATERIAL WHERE id_item = ?", (id_item,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_next_item_id(prefix: str):
        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id_item FROM TABLE_MATERIAL WHERE id_item LIKE ? ORDER BY id_item DESC LIMIT 1",
            (f"{prefix}%",),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return f"{prefix}0001"
        last_id = row[0]
        try:
            num = int(last_id[len(prefix):])
        except ValueError:
            num = 0
        return f"{prefix}{num + 1:04d}"

    @staticmethod
    def update_material_quantity(id_item: str, delta: float):
        status, data = call_json(
            "PATCH",
            f"/materials/{id_item}/quantity",
            payload={"delta": delta},
        )
        if status == 200 and isinstance(data, dict):
            return True, str(data.get("message", "Estoque atualizado com sucesso.")), float(
                data.get("new_quantity", 0)
            )

        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT quantity FROM TABLE_MATERIAL WHERE id_item = ?",
            (id_item,),
        )
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return False, "Item nao encontrado no estoque.", None
        current_qty = float(row[0])
        new_qty = current_qty + float(delta)
        if new_qty < 0:
            cur.close()
            conn.close()
            return False, "Quantidade insuficiente no estoque.", current_qty
        cur.execute(
            "UPDATE TABLE_MATERIAL SET quantity = ? WHERE id_item = ?",
            (new_qty, id_item),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True, "Estoque atualizado com sucesso.", new_qty

