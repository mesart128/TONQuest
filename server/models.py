from typing import Optional

import pydantic


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
