from typing import Optional, TypedDict

from pydantic import BaseModel, Field
from pytoniq_core import Address

from core.types import SystemAddress


class AddAccountSchema(BaseModel):
    address: str


class AccountSchema(BaseModel):
    id: str = Field(..., alias="_id")
    account_address: str
    is_trackable: Optional[bool] = False


class JettonWalletData(TypedDict):
    address: str
    balance: int
    owner: SystemAddress
    jetton_master: SystemAddress
    jetton_wallet_code: str


class InternalTransferMessage(TypedDict):
    op_code: int
    query_id: int
    amount: int
    src: SystemAddress
    response_address: SystemAddress
    forward_ton_amount: int


class NotifyTransferMessage(TypedDict):
    op_code: int
    query_id: int
    amount: int
    sender: Address
    comment: Optional[str]


class TransferMessage(TypedDict):
    op_code: int
    query_id: int
    jetton_amount: int
    destination_address: SystemAddress
    response_address: SystemAddress
    custom_payload: int
    forward_amount: int
    forward_payload: int


class AccountDTO(TypedDict):
    id: str
    account_address: str
    balance: int
    is_trackable: bool


class UpdateAccountSchema(BaseModel):
    is_trackable: bool | None = None
    balance: int | None = None
