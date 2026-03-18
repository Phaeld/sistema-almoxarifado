from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.app.material_service import MaterialService

from ..schemas import (
    MaterialAdjustRequest,
    MaterialCreateRequest,
    MaterialOut,
    MaterialUpdateRequest,
)
from ..security import require_api_key

router = APIRouter(
    prefix="/materials",
    tags=["materials"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", response_model=list[MaterialOut])
def list_materials(
    category_tag: str | None = Query(default=None),
    description: str | None = Query(default=None),
    item_number: str | None = Query(default=None),
    product: str | None = Query(default=None),
    category: str | None = Query(default=None),
) -> list[MaterialOut]:
    rows = MaterialService.get_materials(
        category_tag=category_tag,
        description=description,
        item_number=item_number,
        product=product,
        category=category,
    )
    return [
        MaterialOut(
            id_item=row[0],
            descrption=row[1],
            product=row[2],
            category=row[3],
            quantity=float(row[4]),
            unit_measurement=row[5],
        )
        for row in rows
    ]


@router.post("", response_model=MaterialOut, status_code=status.HTTP_201_CREATED)
def create_material(payload: MaterialCreateRequest) -> MaterialOut:
    MaterialService.create_material(
        id_item=payload.id_item,
        descrption=payload.descrption,
        product=payload.product,
        category=payload.category,
        quantity=payload.quantity,
        unit_measurement=payload.unit_measurement,
    )
    return MaterialOut(**payload.model_dump())


@router.get("/distinct/products", response_model=list[str])
def distinct_products() -> list[str]:
    return MaterialService.get_distinct_products()


@router.get("/distinct/categories", response_model=list[str])
def distinct_categories() -> list[str]:
    return MaterialService.get_distinct_categories()


@router.get("/{id_item}", response_model=MaterialOut)
def get_material(id_item: str) -> MaterialOut:
    row = MaterialService.get_material_by_id(id_item)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found.")
    return MaterialOut(
        id_item=row[0],
        descrption=row[1],
        product=row[2],
        category=row[3],
        quantity=float(row[4]),
        unit_measurement=row[5],
    )


@router.put("/{id_item}", response_model=MaterialOut)
def update_material(id_item: str, payload: MaterialUpdateRequest) -> MaterialOut:
    current = MaterialService.get_material_by_id(id_item)
    if not current:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found.")
    MaterialService.update_material(
        id_item=id_item,
        descrption=payload.descrption,
        product=payload.product,
        category=payload.category,
        quantity=payload.quantity,
        unit_measurement=payload.unit_measurement,
    )
    return MaterialOut(
        id_item=id_item,
        descrption=payload.descrption,
        product=payload.product,
        category=payload.category,
        quantity=payload.quantity,
        unit_measurement=payload.unit_measurement,
    )


@router.delete("/{id_item}")
def delete_material(id_item: str) -> dict[str, str]:
    current = MaterialService.get_material_by_id(id_item)
    if not current:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found.")
    MaterialService.delete_material(id_item)
    return {"message": "Material deleted."}


@router.patch("/{id_item}/quantity")
def adjust_quantity(id_item: str, payload: MaterialAdjustRequest) -> dict[str, str | float]:
    ok, message, new_quantity = MaterialService.update_material_quantity(id_item, payload.delta)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return {"message": message, "new_quantity": float(new_quantity or 0)}
