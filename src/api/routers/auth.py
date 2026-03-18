from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.auth.auth_service import AuthService

from ..schemas import LoginRequest, UserOut
from ..security import require_api_key

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(require_api_key)])


@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest) -> UserOut:
    user = AuthService.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    return UserOut(
        username=user["username"],
        name=user["name"],
        position=user["position"],
        level=int(user["level"]),
        photo=user.get("photo"),
        tag=user.get("tag"),
    )

