from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    name: str
    position: str
    level: int
    photo: bytes | None = None
    tag: str | None = None


class MaterialOut(BaseModel):
    id_item: str
    descrption: str
    product: str
    category: str
    quantity: float
    unit_measurement: str


class MaterialCreateRequest(BaseModel):
    id_item: str
    descrption: str
    product: str
    category: str
    quantity: float = Field(ge=0)
    unit_measurement: str


class MaterialUpdateRequest(BaseModel):
    descrption: str
    product: str
    category: str
    quantity: float = Field(ge=0)
    unit_measurement: str


class MaterialAdjustRequest(BaseModel):
    delta: float


class ActionOut(BaseModel):
    id_action: str
    matter: str
    observation: str | None = None
    category: str
    solocitated: str
    authorized: str
    date: str
    id_item: str
    descrption: str
    quantity: str
    status: str | None = None


class ActionCreateRequest(BaseModel):
    id_action: str | None = None
    prefix: str = Field(pattern="^(ACS|ACE)$")
    matter: str
    observation: str = ""
    category: str
    solocitated: str
    authorized: str
    date_str: str
    id_item: str
    descrption: str
    quantity: str


class ActionStatusRequest(BaseModel):
    status: str = Field(pattern="^(CONFIRMADO|CANCELADO|PENDENTE)$")


class UserListOut(BaseModel):
    id_user: int
    username: str
    name: str
    position: str
    level: int
    tag: str | None = None


class UserCreateRequest(BaseModel):
    username: str
    name: str
    password: str
    position: str
    level: int
    tag: str


class UserUpdateRequest(BaseModel):
    username: str
    name: str
    password: str
    position: str
    level: int
    tag: str


class UserExistsResponse(BaseModel):
    exists: bool


class UserImageUpdateRequest(BaseModel):
    image_base64: str = ""


class VehicleOut(BaseModel):
    id_vehicle: int
    name_vehicle: str
    plate_number: str
    fuel_type: str
    odometer_type: int
    image_vehicle: str | None = None


class VehicleCreateRequest(BaseModel):
    name_vehicle: str
    plate_number: str
    fuel_type: str
    odometer_type: int
    image_vehicle: str | None = None


class ControlOut(BaseModel):
    id_control: int
    name_vehicle: str
    plate_numbler: str
    date: str
    driver: str
    odometer_type: int
    odometer: float
    odometer_difference: str | None = None
    liters_filled: float
    average_consumption: float | None = None
    fuel_type: str
    value: float


class ControlCreateRequest(BaseModel):
    name_vehicle: str
    plate_numbler: str
    date: str
    driver: str
    odometer_type: int
    odometer: float
    odometer_difference: str | None = None
    liters_filled: float
    average_consumption: float | None = None
    fuel_type: str
    value: float
