from typing import Optional

from pydantic import BaseModel, Field


class AddAccountSchema(BaseModel):
    address: str


class AccountSchema(BaseModel):
    id: str = Field(..., alias="_id")
    account_address: str
    is_trackable: Optional[bool] = False
