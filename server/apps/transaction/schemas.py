from typing import List, Literal, Optional, TypedDict


class RawMessageDTO(TypedDict):
    id: Optional[str]
    message_type: Literal["internal", "external"]
    src: str | None
    dest: str
    value: int
    op_code: int
    fwd_fee: int
    created_lt: int
    init: str | None
    body: str


class ParsedTransactionDTO(TypedDict):
    account_id: Optional[str]
    account_address: str
    hash: str
    compute_phase_code: Optional[int]
    action_phase_code: Optional[int]
    total_fee: int
    lt: int
    now: int
    bag_of_cell: str
    in_msg: Optional[RawMessageDTO]
    out_msgs: List[RawMessageDTO]


class RawTransactionDTO(ParsedTransactionDTO):
    id: Optional[str]
    masterchain_seqno: int
    workchain: int
    shard: int
    shard_seqno: int


from pydantic import BaseModel, HttpUrl, UUID4
from typing import List

class Slide(BaseModel):
    id: UUID4
    task_id: UUID4
    title: str
    description: str
    image: HttpUrl
    queue: int

class TaskResponse(BaseModel):
    id: UUID4
    branch_id: UUID4
    title: str
    xp: int
    queue: int
    task_type: str
    action_url: HttpUrl
    call_to_action: str
    slides: List[Slide]

# Example response for documentation
example_response = {
    "id": "0df3ddc1-8e3f-4c01-bbe2-8be289321298",
    "branch_id": "a910dc33-7cbb-41e9-bcab-a3cdfcc46e48",
    "title": "Perform a token swap on Dedust",
    "xp": 100,
    "queue": 1,
    "task_type": "dedust_swap",
    "action_url": "https://dedust.io/register",
    "call_to_action": "You have learned how to change one token for another, keep it up!",
    "slides": [
        {
            "id": "a61dbbef-52a6-453f-bec5-3be1d42a302b",
            "task_id": "0df3ddc1-8e3f-4c01-bbe2-8be289321298",
            "title": "Introduction to Dedust",
            "description": "Learn the basics of decentralized exchanges.",
            "image": "https://kauri.io/images/slide1.png",
            "queue": 1
        }
    ]
}
