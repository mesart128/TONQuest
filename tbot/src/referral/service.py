from pydantic import BaseModel

from src.users.database import get_user_database

REFERRAL_RULES = {
    "default": {
        "reward": 100,
        "reward_limit": None,
        "reward_currency": "NEED",
    }
}


class ReferralRuleSchema(BaseModel):
    name: str
    reward: float
    reward_limit: int | None
    reward_currency: str


async def did_user_get_reward_like_referral(user_id: int):
    # if user exist in database

    user_database = get_user_database()
    user = await user_database.get_user(user_id)
    return bool(user)


async def get_actual_referral_name() -> str:
    return "default"


async def get_referral_rule(referral_name: str) -> dict:
    rule = REFERRAL_RULES.get(referral_name)
    if not rule:
        raise ValueError("Referral rule not found")
    return ReferralRuleSchema(
        name=referral_name,
        reward=rule["reward"],
        reward_limit=rule["reward_limit"],
        reward_currency=rule["reward_currency"],
    )
