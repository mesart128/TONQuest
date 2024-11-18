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
