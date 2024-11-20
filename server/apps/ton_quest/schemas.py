from typing import Optional

import pydantic
from pytoniq_core import Address


class User(pydantic.BaseModel):
    id: int
    name: str
    completed_tasks: list = []
    address: str = ""
    xp: int = 0
    level: int = 0
    profile_photo: str


class CreateUser(pydantic.BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    image: str


class ResponseAllTask(pydantic.BaseModel):
    id: int
    title: str
    icon: str
    description: str
    images: list
    active: bool
    xp: int
    contract_addresses: list
    op_code: Optional[str] = None
    min_amount: float
    parent_id: int | None = None
    external_url: Optional[str] = None
    child_tasks: list = []
    children: list = []


class CompleteTask(pydantic.BaseModel):
    address: str
    op_code: str


class DedustSwapEvent(pydantic.BaseModel):
    event_type: str
    asset_in: Address | None
    asset_out: Address | None
    amount_out: int
    amount_in: int
    sender_address: Address
    op_code: int

    class Config:
        arbitrary_types_allowed = True


