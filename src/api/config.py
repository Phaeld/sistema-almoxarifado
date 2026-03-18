from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    debug: bool
    api_key: str
    allow_origins: list[str]
    project_root: Path


def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    host = os.getenv("ALMOX_API_HOST", "0.0.0.0")
    port = int(os.getenv("ALMOX_API_PORT", "8000"))
    debug = os.getenv("ALMOX_API_DEBUG", "0") == "1"
    api_key = os.getenv("ALMOX_API_KEY", "")
    raw_origins = os.getenv("ALMOX_API_ALLOW_ORIGINS", "*")
    allow_origins = [item.strip() for item in raw_origins.split(",") if item.strip()]
    return Settings(
        host=host,
        port=port,
        debug=debug,
        api_key=api_key,
        allow_origins=allow_origins,
        project_root=project_root,
    )

