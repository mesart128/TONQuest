import enum
from dataclasses import dataclass, field
from typing import List, Literal, Optional, TypedDict

from pytoniq_core import Address


class AccountStateEnum(enum.Enum):
    uninitialized = "uninitialized"
    frozen = "frozen"
    active = "active"


@dataclass
class BlockIdExtDTO:
    file_hash: str
    root_hash: str
    seqno: int
    shard: str
    workchain: int


@dataclass
class TransactionIdDTO:
    hash: str
    lt: str


@dataclass
class FullAccountState:
    extra: Optional[str]
    type: str
    balance: int
    block_id: BlockIdExtDTO
    code: str
    data: str
    frozen_hash: Optional[str]
    last_transaction_id: TransactionIdDTO
    state: Literal["uninitialized", "frozen", "active"]
    sync_utime: int


@dataclass
class SimpleAccountState:
    address: Address
    balance: int
    state: Literal["uninitialized", "frozen", "active"]


@dataclass
class WalletState:
    account_state: AccountStateEnum
    balance: int
    last_transaction_id: TransactionIdDTO
    seqno: Optional[int]
    wallet: bool
    wallet_id: Optional[int]
    wallet_type: Optional[str]


class BlockIdTypedDict(TypedDict):
    type_: str
    file_hash: str
    root_hash: str
    seqno: int
    shard: str
    workchain: int


@dataclass
class ShortTxId:
    type_: str
    account: str
    hash: str
    lt: str
    mode: int


@dataclass
class BlockHeader:
    extra_: str = field(metadata={"name": "@extra"})
    type_: str = field(metadata={"name": "@type"})
    after_merge: bool
    after_split: bool
    before_split: bool
    catchain_seqno: int
    end_lt: str
    flags: int
    gen_utime: int
    global_id: int
    id: BlockIdTypedDict
    is_key_block: bool
    min_ref_mc_seqno: int
    prev_blocks: List[BlockIdTypedDict]
    prev_key_block_seqno: int
    start_lt: str
    validator_list_hash_short: int
    version: int
    want_merge: bool
    want_split: bool
    vert_seqno: Optional[int] = None
