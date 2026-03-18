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

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.app.control_gas_service import ControlGasService

from ..schemas import ControlCreateRequest, ControlOut
from ..security import require_api_key

router = APIRouter(prefix="/controls", tags=["controls"], dependencies=[Depends(require_api_key)])


def _row_to_out(row) -> ControlOut:
    return ControlOut(
        id_control=int(row[0]),
        name_vehicle=row[1],
        plate_numbler=row[2],
        date=row[3],
        driver=row[4],
        odometer_type=int(row[5]),
        odometer=float(row[6]),
        odometer_difference=row[7],
        liters_filled=float(row[8]),
        average_consumption=float(row[9]) if row[9] is not None else None,
        fuel_type=row[10],
        value=float(row[11]),
    )


@router.get("", response_model=list[ControlOut])
def list_controls(
    name_vehicle: str | None = Query(default=None),
    plate_number: str | None = Query(default=None),
    driver: str | None = Query(default=None),
    fuel_type: str | None = Query(default=None),
    date_str: str | None = Query(default=None),
) -> list[ControlOut]:
    rows = ControlGasService.list_controls(
        name_vehicle=name_vehicle,
        plate_number=plate_number,
        driver=driver,
        fuel_type=fuel_type,
        date_str=date_str,
    )
    return [_row_to_out(row) for row in rows]


@router.get("/last-by-plate", response_model=ControlOut)
def last_by_plate(plate_number: str = Query(...), exclude_id: int | None = Query(default=None)) -> ControlOut:
    row = ControlGasService.get_last_control_by_plate(plate_number, exclude_id=exclude_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No control found.")
    return _row_to_out(row)


@router.get("/{control_id}", response_model=ControlOut)
def get_control(control_id: int) -> ControlOut:
    row = ControlGasService.get_control_by_id(control_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Control not found.")
    return _row_to_out(row)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_control(payload: ControlCreateRequest) -> dict[str, str]:
    ControlGasService.create_control(
        name_vehicle=payload.name_vehicle,
        plate_number=payload.plate_numbler,
        date_str=payload.date,
        driver=payload.driver,
        odometer_type=payload.odometer_type,
        odometer=payload.odometer,
        odometer_difference=payload.odometer_difference,
        liters_filled=payload.liters_filled,
        avg_consumption=payload.average_consumption,
        fuel_type=payload.fuel_type,
        value=payload.value,
    )
    return {"message": "Control created."}


@router.put("/{control_id}")
def update_control(control_id: int, payload: ControlCreateRequest) -> dict[str, str]:
    ControlGasService.update_control(
        control_id=control_id,
        name_vehicle=payload.name_vehicle,
        plate_number=payload.plate_numbler,
        date_str=payload.date,
        driver=payload.driver,
        odometer_type=payload.odometer_type,
        odometer=payload.odometer,
        odometer_difference=payload.odometer_difference,
        liters_filled=payload.liters_filled,
        avg_consumption=payload.average_consumption,
        fuel_type=payload.fuel_type,
        value=payload.value,
    )
    return {"message": "Control updated."}


@router.delete("/{control_id}")
def delete_control(control_id: int) -> dict[str, str]:
    ControlGasService.delete_control(control_id)
    return {"message": "Control deleted."}


@router.get("/distinct/fuel-types", response_model=list[str])
def distinct_fuel_types() -> list[str]:
    return ControlGasService.get_distinct_fuel_types()

# Copyright (c) 2026 Raphael da Silva. All rights reserved.
