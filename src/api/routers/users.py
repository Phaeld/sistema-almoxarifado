from __future__ import annotations

import base64

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.auth.auth_service import AuthService

from ..schemas import (
    UserCreateRequest,
    UserExistsResponse,
    UserImageUpdateRequest,
    UserListOut,
    UserUpdateRequest,
)
from ..security import require_api_key

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[UserListOut])
def list_users() -> list[UserListOut]:
    rows = AuthService.list_users()
    return [
        UserListOut(
            id_user=int(row[0]),
            username=row[1],
            name=row[2],
            position=row[3],
            level=int(row[4]),
            tag=row[5],
        )
        for row in rows
    ]


@router.get("/{username}/exists", response_model=UserExistsResponse)
def username_exists(username: str) -> UserExistsResponse:
    return UserExistsResponse(exists=AuthService.username_exists(username))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest) -> dict[str, str]:
    if AuthService.username_exists(payload.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists.")
    AuthService.create_user(
        username=payload.username,
        name=payload.name,
        password=payload.password,
        position=payload.position,
        level=payload.level,
        tag=payload.tag,
    )
    return {"message": "User created."}


@router.put("/{user_id}")
def update_user(user_id: int, payload: UserUpdateRequest) -> dict[str, str]:
    AuthService.update_user(
        user_id=user_id,
        username=payload.username,
        name=payload.name,
        password=payload.password,
        position=payload.position,
        level=payload.level,
        tag=payload.tag,
    )
    return {"message": "User updated."}


@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    AuthService.delete_user(user_id)
    return {"message": "User deleted."}


@router.patch("/{username}/image")
def update_image(username: str, payload: UserImageUpdateRequest) -> dict[str, str]:
    image_bytes = b""
    if payload.image_base64:
        try:
            image_bytes = base64.b64decode(payload.image_base64)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image payload.") from exc
    AuthService.update_user_image(username, image_bytes)
    return {"message": "Image updated."}

