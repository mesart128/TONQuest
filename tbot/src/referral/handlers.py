import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.core.config import env_config
from src.referral.utils import create_referral_message

# from aiogram.utils.i18n import gettext as _

referral_router = Router()


@referral_router.message(Command(commands=["get_referral"]))
async def command_referral(message: Message) -> None:
    text, keyboard = create_referral_message(
        user=message.from_user, channel_name=env_config.telegram.BOT_NICKNAME
    )
    await message.answer(
        text,
        reply_markup=keyboard,
    )


@referral_router.message(Command(commands=["share_referral"]))
async def send_welcome(message: Message):
    logging.info(f"User {message.from_user.id} pressed the 'Share Referral Link' button")
    referral_button = InlineKeyboardButton(text="Get referral link", callback_data="share_referral")

    referral_markup = InlineKeyboardMarkup(inline_keyboard=[[referral_button]])

    await message.answer(
        "Welcome! Press the button below to share your referral link.", reply_markup=referral_markup
    )


@referral_router.callback_query(lambda c: c.data == "share_referral")
async def process_callback_share_referral(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    referral_link = f"https://t.me/{env_config.telegram.BOT_NICKNAME}?start={user_id}"

    from bot import bot

    await bot.send_message(
        callback_query.from_user.id, f"Here is your referral link: {referral_link}"
    )

    await bot.answer_callback_query(callback_query.id)
