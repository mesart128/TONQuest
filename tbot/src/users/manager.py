import logging
from datetime import datetime

from aiogram.types import User

from src.referral.service import get_actual_referral_name, get_referral_rule
from src.users.database import MongoUserDatabase, get_user_database
from src.users.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.users.schemas import CreateUserSchema, ReferrerSchema, UserModelSchema


class UserManager:
    def __init__(self, user_database: MongoUserDatabase):
        self.database = user_database

    async def add_user(self, user: User):
        if await self.get_user(user_id=user.id):
            raise UserAlreadyExistsException("User already exists")
        logging.info(f"Adding user {user.id} to database")
        referral_schema = ReferrerSchema(
            referral_rule_name=await get_actual_referral_name(),
        )
        user_schema = CreateUserSchema(
            chat_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            referral_info=referral_schema,
        )
        await self.database.add_user(user_schema.dict())
        logging.info(f"User {user.id} added to database")
        return await self.get_user(user_id=user.id)

    async def get_user(self, user_id: int) -> UserModelSchema | None:
        user = await self.database.get_user(chat_id=user_id)
        return UserModelSchema(**user) if user else None

    async def update_user_activity(self, user_id: int):
        user: UserModelSchema = await self.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException(user_id)
        user.last_activity = datetime.now()
        await self.database.update_user(chat_id=user_id, dict_to_update=user.dict())
        return await self.get_user(user_id=user_id)

    async def referral_job_done(self, user_id: int):
        user: UserModelSchema = await self.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException(user_id)
        referral_rule = await get_referral_rule(user.referral_info.referral_rule_name)
        user.referral_info.referral_count += 1
        user.balance += referral_rule.reward
        await self.database.update_user(chat_id=user_id, dict_to_update=user.dict())
        return await self.get_user(user_id=user_id)


def get_user_manager() -> UserManager:
    return UserManager(get_user_database())
