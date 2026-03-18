from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.app.vehicle_service import VehicleService

from ..schemas import VehicleCreateRequest, VehicleOut
from ..security import require_api_key

router = APIRouter(prefix="/vehicles", tags=["vehicles"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[VehicleOut])
def list_vehicles() -> list[VehicleOut]:
    rows = VehicleService.list_vehicles()
    return [
        VehicleOut(
            id_vehicle=int(row[0]),
            name_vehicle=row[1],
            plate_number=row[2],
            fuel_type=row[3],
            odometer_type=int(row[4]),
            image_vehicle=row[5],
        )
        for row in rows
    ]


@router.get("/by-plate", response_model=VehicleOut)
def get_by_plate(plate_number: str = Query(...)) -> VehicleOut:
    row = VehicleService.get_vehicle_by_plate(plate_number)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    return VehicleOut(
        id_vehicle=int(row[0]),
        name_vehicle=row[1],
        plate_number=row[2],
        fuel_type=row[3],
        odometer_type=int(row[4]),
        image_vehicle=row[5],
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: VehicleCreateRequest) -> dict[str, str]:
    VehicleService.create_vehicle(
        name=payload.name_vehicle,
        plate=payload.plate_number,
        fuel_type=payload.fuel_type,
        odometer_type=payload.odometer_type,
        image_path=payload.image_vehicle,
    )
    return {"message": "Vehicle created."}


@router.put("/{vehicle_id}")
def update_vehicle(vehicle_id: int, payload: VehicleCreateRequest) -> dict[str, str]:
    VehicleService.update_vehicle(
        vehicle_id=vehicle_id,
        name=payload.name_vehicle,
        plate=payload.plate_number,
        fuel_type=payload.fuel_type,
        odometer_type=payload.odometer_type,
        image_path=payload.image_vehicle,
    )
    return {"message": "Vehicle updated."}


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int) -> dict[str, str]:
    VehicleService.delete_vehicle(vehicle_id)
    return {"message": "Vehicle deleted."}


@router.get("/distinct/fuel-types", response_model=list[str])
def distinct_fuel_types() -> list[str]:
    return VehicleService.get_distinct_fuel_types()


@router.get("/distinct/odometer-types", response_model=list[int])
def distinct_odometer_types() -> list[int]:
    return VehicleService.get_distinct_odometer_types()


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int) -> VehicleOut:
    row = VehicleService.get_vehicle_by_id(vehicle_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    return VehicleOut(
        id_vehicle=int(row[0]),
        name_vehicle=row[1],
        plate_number=row[2],
        fuel_type=row[3],
        odometer_type=int(row[4]),
        image_vehicle=row[5],
    )
