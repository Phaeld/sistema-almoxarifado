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


# Copyright (c) 2026 Raphael da Silva. All rights reserved.
