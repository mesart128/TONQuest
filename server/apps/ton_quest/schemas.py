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

class Piece(pydantic.BaseModel):
    id: UUID
    nft_id: UUID
    image: str
    branch_id: Optional[str]
    queue: Optional[int]

class NFT(pydantic.BaseModel):
    id: UUID
    image: str
    contract_address: str
    pieces: List[Piece]

class Branch(pydantic.BaseModel):
    id: UUID
    category_id: UUID
    tasks: List[Task]

class Category(pydantic.BaseModel):
    id: UUID
    head: str
    title: str
    description: str
    image: str
    subtitle: str
    branches: List[Branch]

class SuccessResponse(pydantic.BaseModel):
    success: bool

class ErrorResponse(pydantic.BaseModel):
    error: str

class IsCompletedResponse(pydantic.BaseModel):
    completed: bool

class DedustEvent(pydantic.BaseModel):
    event_type: str
    asset_in: str
    asset_out: int
    amount_out: int
    amount_in: int
    sender_address: str
    op_code: str
