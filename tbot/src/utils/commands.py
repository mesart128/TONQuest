from aiogram import Bot
from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Go Go Go 🚀"),
        BotCommand(command="get_referral", description="Get referral link 🤑"),
        # BotCommand(command="reward", description="Get test jettons 💰"),
        # BotCommand(command="share_referral", description="Share referral link 📢"),
    ]
    await bot(SetMyCommands(commands=commands))
