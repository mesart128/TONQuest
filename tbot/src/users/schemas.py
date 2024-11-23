from datetime import datetime

from pydantic import BaseModel, Field


class ReferrerSchema(BaseModel):
    referral_count: int = 0
    referral_rule_name: str


class UserModelSchema(BaseModel):
    chat_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    balance: int
    referral_info: ReferrerSchema
    created: datetime
    updated: datetime | None
    last_activity: datetime | None


class CreateUserSchema(BaseModel):
    chat_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    balance: int = 0
    referral_info: ReferrerSchema
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime | None = Field(default_factory=datetime.now)
    last_activity: datetime | None = Field(default_factory=datetime.now)
