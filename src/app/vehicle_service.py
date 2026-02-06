"""
====================================================================
    VEHICLE SERVICE
--------------------------------------------------------------------
    Funções de acesso à tabela TABLE_VEHICLES do banco vehicles.db
====================================================================
"""

import os
import sqlite3

CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "vehicles.db")


class VehicleService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def list_vehicles():
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
        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TABLE_VEHICLES WHERE id_vehicle = ?", (vehicle_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_distinct_fuel_types():
        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT fuel_type FROM TABLE_VEHICLES ORDER BY fuel_type")
        values = [row[0] for row in cur.fetchall() if row[0]]
        cur.close()
        conn.close()
        return values

    @staticmethod
    def get_distinct_odometer_types():
        conn = VehicleService.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT odometer_type FROM TABLE_VEHICLES ORDER BY odometer_type")
        values = [row[0] for row in cur.fetchall() if row[0] is not None]
        cur.close()
        conn.close()
        return values
