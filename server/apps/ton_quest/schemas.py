from typing import List, Optional
from uuid import UUID

import pydantic


class User(pydantic.BaseModel):
    id: UUID
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    image: str
    wallet_address: Optional[str] = None
    completed_tasks: List[UUID] = []
    claimed_tasks: List[UUID] = []
    completed_branches: List[UUID] = []
    claimed_pieces: List[UUID] = []
    nfts: List[UUID] = []

class Slide(pydantic.BaseModel):
    id: UUID
    task_id: UUID
    title: str
    description: str
    image: str
    queue: int

    class Config:
        from_attributes = True

class Task(pydantic.BaseModel):
    id: UUID
    branch_id: UUID
    title: str
    xp: int
    queue: int
    task_type: str
    action_url: str
    call_to_action: str
    slides: List[Slide]

    class Config:
        from_attributes = True

class Piece(pydantic.BaseModel):
    id: UUID
    nft_id: UUID
    image: str
    branch_id: Optional[str]
    queue: Optional[int]

    class Config:
        from_attributes = True

class NFT(pydantic.BaseModel):
    id: UUID
    image: str
    contract_address: str
    pieces: List[Piece]

    class Config:
        from_attributes = True

class Branch(pydantic.BaseModel):
    id: UUID
    category_id: UUID
    tasks: List[Task]

    class Config:
        from_attributes = True

class Category(pydantic.BaseModel):
    id: UUID
    head: str
    title: str
    description: str
    image: str
    subtitle: str
    branches: List[Branch]

    class Config:
        from_attributes = True



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


class DedustEvent(pydantic.BaseModel):
    event_type: str
    asset_in: str
    asset_out: int
    amount_out: int
    amount_in: int
    sender_address: str
    op_code: str
