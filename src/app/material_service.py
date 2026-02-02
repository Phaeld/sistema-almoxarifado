"""
====================================================================
    MATERIAL SERVICE
--------------------------------------------------------------------
    Funções de acesso à tabela TABLE_MATERIAL do banco material.db
====================================================================
"""

import os
import sqlite3


# -----------------------------------------------------------------
#  Caminho do banco material.db
#  Estrutura esperada:
#  sistema-almoxarifado/
#       database/material.db
#       src/app/material_service.py (este arquivo)
# -----------------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)          # .../src/app
SRC_DIR = os.path.dirname(CURRENT_DIR)           # .../src
PROJECT_ROOT = os.path.dirname(SRC_DIR)          # .../sistema-almoxarifado
DB_PATH = os.path.join(PROJECT_ROOT, "database", "material.db")


# -----------------------------------------------------------------
#  MAPA DE TAGS -> PREFIXO DO id_item
#  Ex.: ELE -> 'E%'  (E0001, E0002...)
# -----------------------------------------------------------------
CATEGORY_PREFIX_MAP = {
    "LIM": "L",   # Limpeza, Higiene & Alimentos  (ex.: L0001)
    "ELE": "E",   # Elétrica                      (ex.: E0001)
    "HID": "H",   # Hidráulica                    (ex.: H0001)
    "FER": "F",   # Ferramentas Gerais            (ex.: F0001)
    "AUT": "A",   # Automóveis                    (ex.: A0001)
    # se tiver mais categorias, só adicionar aqui
}


class MaterialService:

    @staticmethod
    def get_connection():
        """Abre conexão com o banco de materiais."""
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def get_materials(
        category_tag=None,
        description=None,
        item_number=None,
        product=None,
        category=None,
    ):
        """
        Busca materiais na TABLE_MATERIAL aplicando filtros.

        Parâmetros:
            category_tag  -> tag da Home / sidebar (ELE, HID, LIM...)
            description   -> filtro por texto na coluna 'descreption'
            item_number   -> filtro por id_item (E001, H002, etc.)
            product       -> filtro exato na coluna 'product'
            category      -> filtro exato na coluna 'category'

        Retorno:
            lista de tuplas:
            (id_item, descreption, product, category, quantity, unit_measurement)
        """

        conn = MaterialService.get_connection()
        cur = conn.cursor()

        # Atenção: coluna se chama 'descreption' no banco (typo)
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

        # Filtro pela TAG (prefixo do id_item)
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

    # Opcional: funções para preencher combos depois
    @staticmethod
    def get_distinct_products():
        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT product FROM TABLE_MATERIAL ORDER BY product")
        values = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def get_distinct_categories():
        conn = MaterialService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM TABLE_MATERIAL ORDER BY category")
        values = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def update_material_quantity(id_item: str, delta: float):
        """
        Atualiza a quantidade de um item somando o delta (pode ser negativo).
        Retorna (ok: bool, message: str, new_quantity: float | None).
        """
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
            return False, "Item não encontrado no estoque.", None

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
