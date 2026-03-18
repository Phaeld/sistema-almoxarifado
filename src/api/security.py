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

from fastapi import Header, HTTPException, status

from .config import get_settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.api_key:
        return
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )


# Copyright (c) 2026 Raphael da Silva. All rights reserved.
