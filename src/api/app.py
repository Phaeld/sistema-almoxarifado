from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .schemas import HealthResponse

os.environ["ALMOX_API_DISABLE_CLIENT"] = "1"

from .routers import actions, auth, controls, materials, users, vehicles

settings = get_settings()

app = FastAPI(
    title="Almoxarifado API",
    version="0.1.0",
    description="API central para acesso multi-maquina aos bancos SQLite.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(materials.router)
app.include_router(actions.router)
app.include_router(vehicles.router)
app.include_router(controls.router)
