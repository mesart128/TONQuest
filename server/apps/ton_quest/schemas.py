from typing import Optional

import pydantic


class User(pydantic.BaseModel):
    id: int
    name: str
    completed_tasks: list = []
    address: str = ""
    xp: int = 0
    level: int = 0
    profile_photo: str


class CreateUser(pydantic.BaseModel):
    id: int
    name: str
    profile_photo: str


class Task(pydantic.BaseModel):
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
