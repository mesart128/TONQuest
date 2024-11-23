import re
from typing import Tuple

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, User


def extract_user_id(referral_url):
    pattern = r"\?start=(\d+)"

    match = re.search(pattern, referral_url)

    if match:
        return match.group(1)
    else:
        return None


def get_referral_link(user: User, channel_name: str) -> str:
    return f"https://t.me/{channel_name}?start={user.id}"


def create_referral_message(user: User, channel_name: str) -> Tuple[str, ReplyKeyboardMarkup]:
    referral_link = get_referral_link(user, channel_name)
    text_english = (
        f"🎉 Congratulations! You have successfully registered in our service! "
        f"Your referral code: {referral_link}.\n"
        "Invite friends → We will onboard them → Both parties receive rewards. \n\n"
        "To do this, send them your referral code and ask them to specify it when registering.\n"
        f"Your referral code: {referral_link}.\n"
        "Lets learn to earn! 🚀"
    )
    keyboard_buttons = [
        [KeyboardButton(text="Invite friends", url=referral_link)],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)
    return text_english, keyboard
