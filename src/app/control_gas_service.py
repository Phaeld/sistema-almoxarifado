"""
====================================================================
    CONTROL GAS SERVICE
--------------------------------------------------------------------
    Funções de acesso à tabela TABLE_CONTROL_GAS do banco control.db
====================================================================
"""

import os
import sqlite3

CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "control.db")


class ControlGasService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def list_controls(
        name_vehicle=None,
        plate_number=None,
        driver=None,
        fuel_type=None,
        date_str=None,
    ):
        conn = ControlGasService.get_connection()
        cur = conn.cursor()

        query = """
            SELECT
                id_control,
                name_vehicle,
                plate_numbler,
                date,
                driver,
                odometer_type,
                odometer,
                odometer_difference,
                liters_filled,
                "average consumption",
                fuel_type,
                value
            FROM TABLE_CONTROL_GAS
            WHERE 1 = 1
        """
        params = []

        if name_vehicle:
            query += " AND name_vehicle LIKE ?"
            params.append(f"%{name_vehicle}%")

        if plate_number:
            query += " AND plate_numbler LIKE ?"
            params.append(f"%{plate_number}%")

        if driver:
            query += " AND driver LIKE ?"
            params.append(f"%{driver}%")

        if fuel_type and fuel_type != "Selecione":
            query += " AND fuel_type = ?"
            params.append(fuel_type)

        if date_str:
            query += " AND date = ?"
            params.append(date_str)

        query += " ORDER BY id_control DESC"

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_control_by_id(control_id: int):
        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                id_control,
                name_vehicle,
                plate_numbler,
                date,
                driver,
                odometer_type,
                odometer,
                odometer_difference,
                liters_filled,
                "average consumption",
                fuel_type,
                value
            FROM TABLE_CONTROL_GAS
            WHERE id_control = ?
            """,
            (control_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def create_control(
        name_vehicle,
        plate_number,
        date_str,
        driver,
        odometer_type,
        odometer,
        odometer_difference,
        liters_filled,
        avg_consumption,
        fuel_type,
        value,
    ):
        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO TABLE_CONTROL_GAS (
                name_vehicle,
                plate_numbler,
                date,
                driver,
                odometer_type,
                odometer,
                odometer_difference,
                liters_filled,
                "average consumption",
                fuel_type,
                value
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name_vehicle,
                plate_number,
                date_str,
                driver,
                odometer_type,
                odometer,
                odometer_difference,
                liters_filled,
                avg_consumption,
                fuel_type,
                value,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update_control(
        control_id,
        name_vehicle,
        plate_number,
        date_str,
        driver,
        odometer_type,
        odometer,
        odometer_difference,
        liters_filled,
        avg_consumption,
        fuel_type,
        value,
    ):
        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE TABLE_CONTROL_GAS
            SET
                name_vehicle = ?,
                plate_numbler = ?,
                date = ?,
                driver = ?,
                odometer_type = ?,
                odometer = ?,
                odometer_difference = ?,
                liters_filled = ?,
                "average consumption" = ?,
                fuel_type = ?,
                value = ?
            WHERE id_control = ?
            """,
            (
                name_vehicle,
                plate_number,
                date_str,
                driver,
                odometer_type,
                odometer,
                odometer_difference,
                liters_filled,
                avg_consumption,
                fuel_type,
                value,
                control_id,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_control(control_id: int):
        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TABLE_CONTROL_GAS WHERE id_control = ?", (control_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_distinct_fuel_types():
        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT fuel_type FROM TABLE_CONTROL_GAS ORDER BY fuel_type")
        values = [row[0] for row in cur.fetchall() if row[0]]
        cur.close()
        conn.close()
        return values
