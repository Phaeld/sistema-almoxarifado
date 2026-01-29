# material_service.py
"""
Serviço de acesso à tabela TABLE_MATERIAL
"""

import sqlite3
import os

# ⚠️ IMPORTA O MESMO DB_PATH DO LOGIN
# from auth.auth_service import DB_PATH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "material.db")

class MaterialService:
    @staticmethod
    def get_materials(
        category_prefix: str = "",
        description: str = "",
        id_item: str = "",
        product: str = "",
    ):
        """
        Busca materiais na TABLE_MATERIAL.

        - category_prefix: prefixo do id_item (E, H, L, F, A...)
        - description, id_item, product: filtros opcionais
        """

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

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

        # prefixo da categoria (E, H, L...)
        if category_prefix:
            query += " AND id_item LIKE ?"
            params.append(category_prefix + "%")

        if description:
            query += " AND descreption LIKE ?"
            params.append(f"%{description}%")

        if id_item:
            query += " AND id_item LIKE ?"
            params.append(f"%{id_item}%")

        if product:
            query += " AND product LIKE ?"
            params.append(f"%{product}%")

        cursor.execute(query, params)
        rows = cursor.fetchall()

        conn.close()
        return rows
