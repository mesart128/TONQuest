from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from src.core.config import env_config
from src.core.messages import get_welcome_keyboard, get_welcome_message
from src.referral.state import RewardStates
from src.referral.utils import get_referral_link
from src.users.manager import get_user_manager

main_router = Router()

#
# async def message_for_testing_purpose(message: Message) -> None:
#     await message.answer(
#         "For testing purpose you will need test jettons. \n"
#         "Please use command /reward to get jUSDT and jNEED. \n",
#     )
#
#
# @main_router.message(Command(commands=["reward"]))
# async def command_reward(message: Message, state: FSMContext) -> None:
#     await state.set_state(RewardStates.write_reward)
#     await message.answer("Write you address to get test jettons. \n")
#
#
# @main_router.message(RewardStates.write_reward)
# async def write_reward(message: Message, state: FSMContext) -> None:
#     from bot import bot
#
#     # send message to ADMIN
#     await bot.send_message(
#         chat_id=env_config.telegram.ADMIN_ID,
#         text=f"User {message.from_user.id} wants to get test jettons. Address: {message.text}",
#     )
#     await message.answer("Wait for test jettons. It will coming soon. \n")
#     await state.clear()


@main_router.message(Command(commands=["start"]))
async def command_start(message: Message) -> None:
    # await state.clear()
    from bot import bot
    await bot.send_message(
                chat_id=env_config.telegram.ADMIN_ID,
                text=f"User {message.from_user.id} started bot. ",
            )
    await message.answer(f"Hello {message.from_user.first_name}! \n" f"Welcome to our bot. \n",
                         reply_markup=get_welcome_keyboard())
    # user_manager = get_user_manager()
    # exist_user = await user_manager.get_user(message.from_user.id)
    # if not exist_user:
    #     if message.chat.type == "private":
    #         start_command = message.text
    #         referrer_id = str(start_command[7:])
    #         if referrer_id != "":
    #             await user_manager.referral_job_done(user_id=int(referrer_id))
    #             await user_manager.add_user(user=message.from_user)
    #             referral_link = get_referral_link(
    #                 user=message.from_user, channel_name=env_config.telegram.BOT_NICKNAME
    #             )
    #             user = await user_manager.get_user(message.from_user.id)
    #             await message.answer(
    #                 f"Welcome {message.from_user.first_name}!,"
    #                 " Your friend already got reward. You can too. \n"
    #                 f"Your referral link: {referral_link}. \n"
    #                 f"You current balance is {user.balance} NEED. \n"
    #                 f"LInk to application: {env_config.telegram.WEB_APP_URL} \n",
    #                 reply_markup=ReplyKeyboardMarkup(
    #                     keyboard=[[KeyboardButton(text="Invite friends", url=referral_link)]],
    #                     resize_keyboard=True,
    #                 ),
    #             )
    #             await message_for_testing_purpose(message)
    #             return
    #         else:
    #             await user_manager.add_user(user=message.from_user)
    #             await message.answer(
    #                 text=get_welcome_message(),
    #                 reply_markup=get_welcome_keyboard(),
    #             )
    #             await message_for_testing_purpose(message)
    #             return
    # else:
    #     referral_link = get_referral_link(
    #         user=message.from_user, channel_name=env_config.telegram.BOT_NICKNAME
    #     )
    #     user = await user_manager.get_user(message.from_user.id)
    #     await message.answer(
    #         "You are already in our system. You can invite friends and get rewards. \n"
    #         f"You balance: {user.balance} NEED. \n"
    #         f"Your referral link to invite friends: {referral_link}. \n"
    #         f"You can browse our app and progress in by the button below.\n"
    #         f"Link to application: {env_config.telegram.WEB_APP_URL} \n",
    #         reply_markup=InlineKeyboardMarkup(
    #             inline_keyboard=[
    #                 [InlineKeyboardButton(text="Open App", url=env_config.telegram.WEB_APP_URL)]
    #             ]
    #         ),
    #     )
    #     await message_for_testing_purpose(message)
