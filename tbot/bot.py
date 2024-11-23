import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest

from src.core.config import env_config
from src.core.database import redis_storage
from src.core.handlers import main_router
from src.core.logger_settings import setup_logging
from src.referral.handlers import referral_router
from src.utils.commands import set_commands

# Bot token can be obtained via https://t.me/BotFather
TOKEN = env_config.telegram.BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


async def check_the_user_is_subscriber(bot: Bot, channel_id: int, user_id: int):
    try:
        result = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if (
            result.status == ChatMemberStatus.MEMBER
            or result.status == ChatMemberStatus.CREATOR
            or result.status == ChatMemberStatus.ADMINISTRATOR
        ):
            logging.info(f"User {user_id} is a subscriber of the channel {channel_id}")
            return True
        else:
            return False
    except TelegramBadRequest:
        logging.info(f"User {user_id} is not a subscriber of the channel {channel_id}")
        return False


@dp.channel_post()
async def echo(message: types.Message):
    await check_the_user_is_subscriber(
        bot, env_config.telegram.CHANNEL_ID, env_config.telegram.ADMIN_ID
    )
    await message.answer(message.text)


async def on_startup():
    logging.warning("Starting connection")
    dp.include_router(main_router)
    dp.include_router(referral_router)
    logging.warning("Connection established")


bot = Bot(TOKEN)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    await set_commands(bot)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
