# ============================================================================
# Author: Raphael da Silva
# Copyright (c) 2026 Raphael da Silva. All rights reserved.
# Proprietary and confidential software.
# Unauthorized use, copying, modification, distribution, disclosure,
# reverse engineering, sublicensing, or commercialization of this source code,
# in whole or in part, is strictly prohibited without prior written permission.
# This work is protected under Brazilian Software Law (Law No. 9,609/1998),
# Brazilian Copyright Law (Law No. 9,610/1998), and other applicable laws.
# ============================================================================

"""
====================================================================
    CONTROL GAS SERVICE
--------------------------------------------------------------------
    FunÃ§Ãµes de acesso Ã  tabela TABLE_CONTROL_GAS do banco control.db
====================================================================
"""

import os
import sqlite3
from datetime import datetime
try:
    from .remote_api import call_json
    from .runtime_paths import database_path
except ImportError:
    from remote_api import call_json
    from runtime_paths import database_path

DB_PATH = database_path("control.db")


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
        status, data = call_json(
            "GET",
            "/controls",
            params={
                "name_vehicle": name_vehicle,
                "plate_number": plate_number,
                "driver": driver,
                "fuel_type": fuel_type,
                "date_str": date_str,
            },
        )
        if status == 200 and isinstance(data, list):
            return [
                (
                    int(row.get("id_control", 0)),
                    row.get("name_vehicle", ""),
                    row.get("plate_numbler", ""),
                    row.get("date", ""),
                    row.get("driver", ""),
                    int(row.get("odometer_type", 0)),
                    float(row.get("odometer", 0)),
                    row.get("odometer_difference"),
                    row.get("liters_filled", 0),
                    row.get("average_consumption"),
                    row.get("fuel_type", ""),
                    float(row.get("value", 0)),
                )
                for row in data
            ]

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
        status, data = call_json("GET", f"/controls/{control_id}")
        if status == 200 and isinstance(data, dict):
            return (
                int(data.get("id_control", 0)),
                data.get("name_vehicle", ""),
                data.get("plate_numbler", ""),
                data.get("date", ""),
                data.get("driver", ""),
                int(data.get("odometer_type", 0)),
                float(data.get("odometer", 0)),
                data.get("odometer_difference"),
                data.get("liters_filled", 0),
                data.get("average_consumption"),
                data.get("fuel_type", ""),
                float(data.get("value", 0)),
            )

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
    def get_last_control_by_plate(plate_number: str, exclude_id: int | None = None):
        status, data = call_json(
            "GET",
            "/controls/last-by-plate",
            params={"plate_number": plate_number, "exclude_id": exclude_id},
        )
        if status == 200 and isinstance(data, dict):
            return (
                int(data.get("id_control", 0)),
                data.get("name_vehicle", ""),
                data.get("plate_numbler", ""),
                data.get("date", ""),
                data.get("driver", ""),
                int(data.get("odometer_type", 0)),
                float(data.get("odometer", 0)),
                data.get("odometer_difference"),
                data.get("liters_filled", 0),
                data.get("average_consumption"),
                data.get("fuel_type", ""),
                float(data.get("value", 0)),
            )

        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        params = [plate_number]
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
            WHERE plate_numbler = ?
        """
        if exclude_id:
            query += " AND id_control != ?"
            params.append(exclude_id)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return None

        def parse_date(value: str):
            try:
                return datetime.strptime(value, "%d/%m/%Y")
            except (TypeError, ValueError):
                return datetime.min

        rows.sort(key=lambda r: parse_date(r[3]), reverse=True)
        return rows[0]

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
        status, _ = call_json(
            "POST",
            "/controls",
            payload={
                "name_vehicle": name_vehicle,
                "plate_numbler": plate_number,
                "date": date_str,
                "driver": driver,
                "odometer_type": int(odometer_type),
                "odometer": float(odometer),
                "odometer_difference": odometer_difference,
                "liters_filled": liters_filled,
                "average_consumption": avg_consumption,
                "fuel_type": fuel_type,
                "value": float(value),
            },
        )
        if status == 201:
            return

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
        status, _ = call_json(
            "PUT",
            f"/controls/{control_id}",
            payload={
                "name_vehicle": name_vehicle,
                "plate_numbler": plate_number,
                "date": date_str,
                "driver": driver,
                "odometer_type": int(odometer_type),
                "odometer": float(odometer),
                "odometer_difference": odometer_difference,
                "liters_filled": liters_filled,
                "average_consumption": avg_consumption,
                "fuel_type": fuel_type,
                "value": float(value),
            },
        )
        if status == 200:
            return

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
        status, _ = call_json("DELETE", f"/controls/{control_id}")
        if status == 200:
            return

        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TABLE_CONTROL_GAS WHERE id_control = ?", (control_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_distinct_fuel_types():
        status, data = call_json("GET", "/controls/distinct/fuel-types")
        if status == 200 and isinstance(data, list):
            return [str(v) for v in data]

        conn = ControlGasService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT fuel_type FROM TABLE_CONTROL_GAS ORDER BY fuel_type")
        values = [row[0] for row in cur.fetchall() if row[0]]
        cur.close()
        conn.close()
        return values

# Copyright (c) 2026 Raphael da Silva. All rights reserved.
