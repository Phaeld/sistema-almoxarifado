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
    VEHICLE SERVICE
--------------------------------------------------------------------
    FunÃ§Ãµes de acesso Ã  tabela TABLE_VEHICLES do banco vehicles.db
====================================================================
"""

import os
import sqlite3
try:
    from .remote_api import call_json
    from .runtime_paths import database_path
except ImportError:
    from remote_api import call_json
    from runtime_paths import database_path

DB_PATH = database_path("vehicles.db")


class VehicleService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def list_vehicles():
        status, data = call_json("GET", "/vehicles")
        if status == 200 and isinstance(data, list):
            return [
                (
                    int(row.get("id_vehicle", 0)),
                    row.get("name_vehicle", ""),
                    row.get("plate_number", ""),
                    row.get("fuel_type", ""),
                    int(row.get("odometer_type", 0)),
                    row.get("image_vehicle"),
                )
                for row in data
            ]

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                id_vehicle,
                name_vehicle,
                plate_number,
                fuel_type,
                odometer_type,
                image_vehicle
            FROM TABLE_VEHICLES
            ORDER BY name_vehicle
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_vehicle_by_id(vehicle_id: int):
        status, data = call_json("GET", f"/vehicles/{vehicle_id}")
        if status == 200 and isinstance(data, dict):
            return (
                int(data.get("id_vehicle", 0)),
                data.get("name_vehicle", ""),
                data.get("plate_number", ""),
                data.get("fuel_type", ""),
                int(data.get("odometer_type", 0)),
                data.get("image_vehicle"),
            )

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                id_vehicle,
                name_vehicle,
                plate_number,
                fuel_type,
                odometer_type,
                image_vehicle
            FROM TABLE_VEHICLES
            WHERE id_vehicle = ?
            """,
            (vehicle_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def get_vehicle_by_plate(plate_number: str):
        status, data = call_json("GET", "/vehicles/by-plate", params={"plate_number": plate_number})
        if status == 200 and isinstance(data, dict):
            return (
                int(data.get("id_vehicle", 0)),
                data.get("name_vehicle", ""),
                data.get("plate_number", ""),
                data.get("fuel_type", ""),
                int(data.get("odometer_type", 0)),
                data.get("image_vehicle"),
            )

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                id_vehicle,
                name_vehicle,
                plate_number,
                fuel_type,
                odometer_type,
                image_vehicle
            FROM TABLE_VEHICLES
            WHERE plate_number = ?
            """,
            (plate_number,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def create_vehicle(name, plate, fuel_type, odometer_type, image_path=None):
        status, _ = call_json(
            "POST",
            "/vehicles",
            payload={
                "name_vehicle": name,
                "plate_number": plate,
                "fuel_type": fuel_type,
                "odometer_type": int(odometer_type),
                "image_vehicle": image_path,
            },
        )
        if status == 201:
            return

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO TABLE_VEHICLES
                (name_vehicle, plate_number, fuel_type, odometer_type, image_vehicle)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, plate, fuel_type, odometer_type, image_path),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update_vehicle(vehicle_id, name, plate, fuel_type, odometer_type, image_path=None):
        status, _ = call_json(
            "PUT",
            f"/vehicles/{vehicle_id}",
            payload={
                "name_vehicle": name,
                "plate_number": plate,
                "fuel_type": fuel_type,
                "odometer_type": int(odometer_type),
                "image_vehicle": image_path,
            },
        )
        if status == 200:
            return

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE TABLE_VEHICLES
            SET name_vehicle = ?, plate_number = ?, fuel_type = ?, odometer_type = ?, image_vehicle = ?
            WHERE id_vehicle = ?
            """,
            (name, plate, fuel_type, odometer_type, image_path, vehicle_id),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_vehicle(vehicle_id: int):
        status, _ = call_json("DELETE", f"/vehicles/{vehicle_id}")
        if status == 200:
            return

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TABLE_VEHICLES WHERE id_vehicle = ?", (vehicle_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_distinct_fuel_types():
        status, data = call_json("GET", "/vehicles/distinct/fuel-types")
        if status == 200 and isinstance(data, list):
            return [str(v) for v in data]

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT fuel_type FROM TABLE_VEHICLES ORDER BY fuel_type")
        values = [row[0] for row in cur.fetchall() if row[0]]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def get_distinct_odometer_types():
        status, data = call_json("GET", "/vehicles/distinct/odometer-types")
        if status == 200 and isinstance(data, list):
            return [int(v) for v in data]

        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT odometer_type FROM TABLE_VEHICLES ORDER BY odometer_type")
        values = [row[0] for row in cur.fetchall() if row[0] is not None]
        cur.close()
        conn.close()
        return values

# Copyright (c) 2026 Raphael da Silva. All rights reserved.
