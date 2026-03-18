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

from src.app.action_service import ActionService

from ..schemas import ActionCreateRequest, ActionOut, ActionStatusRequest
from ..security import require_api_key

router = APIRouter(prefix="/actions", tags=["actions"], dependencies=[Depends(require_api_key)])


@router.get("/next-id/{prefix}")
def next_action_id(prefix: str) -> dict[str, str]:
    if prefix not in {"ACS", "ACE"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid prefix.")
    return {"id_action": ActionService.get_next_action_id(prefix)}


@router.get("", response_model=list[ActionOut])
def list_actions(
    subject: str | None = Query(default=None),
    id_action: str | None = Query(default=None),
    observation: str | None = Query(default=None),
    date_str: str | None = Query(default=None),
) -> list[ActionOut]:
    rows = ActionService.list_actions()
    if subject:
        rows = [r for r in rows if subject.lower() in str(r[1] or "").lower()]
    if id_action:
        rows = [r for r in rows if id_action.lower() in str(r[0] or "").lower()]
    if observation:
        rows = [r for r in rows if observation.lower() in str(r[2] or "").lower()]
    if date_str:
        rows = [r for r in rows if str(r[6] or "") == date_str]
    return [
        ActionOut(
            id_action=row[0],
            matter=row[1],
            observation=row[2],
            category=row[3],
            solocitated=row[4],
            authorized=row[5],
            date=row[6],
            id_item=row[7],
            descrption=row[8],
            quantity=str(row[9]),
            status=row[10],
        )
        for row in rows
    ]


@router.get("/{id_action}", response_model=ActionOut)
def get_action(id_action: str) -> ActionOut:
    row = ActionService.get_action_by_id(id_action)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found.")
    return ActionOut(
        id_action=row[0],
        matter=row[1],
        observation=row[2],
        category=row[3],
        solocitated=row[4],
        authorized=row[5],
        date=row[6],
        id_item=row[7],
        descrption=row[8],
        quantity=str(row[9]),
        status=row[10],
    )


@router.post("", response_model=ActionOut, status_code=status.HTTP_201_CREATED)
def create_action(payload: ActionCreateRequest) -> ActionOut:
    new_id = payload.id_action or ActionService.get_next_action_id(payload.prefix)
    ActionService.insert_action(
        id_action=new_id,
        matter=payload.matter,
        observation=payload.observation,
        category=payload.category,
        solocitated=payload.solocitated,
        authorized=payload.authorized,
        date_str=payload.date_str,
        id_item=payload.id_item,
        descrption=payload.descrption,
        quantity=payload.quantity,
    )
    row = ActionService.get_action_by_id(new_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load action.")
    return ActionOut(
        id_action=row[0],
        matter=row[1],
        observation=row[2],
        category=row[3],
        solocitated=row[4],
        authorized=row[5],
        date=row[6],
        id_item=row[7],
        descrption=row[8],
        quantity=str(row[9]),
        status=row[10],
    )


@router.patch("/{id_action}/status")
def update_status(id_action: str, payload: ActionStatusRequest) -> dict[str, str]:
    row = ActionService.get_action_by_id(id_action)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found.")
    ActionService.update_action_status(id_action, payload.status)
    return {"message": "Status updated.", "id_action": id_action, "status": payload.status}

# Copyright (c) 2026 Raphael da Silva. All rights reserved.
