from config import MONGO_URI
from database import CustomMotorClient
from apps.ton_quest.schemas import Task

import random
from enum import IntEnum

db= CustomMotorClient(MONGO_URI)



class OpCodes(IntEnum):
    # JETTON messages
    default_message = 0x00000000

    # TonCrypto
    dedust_swap = 0x9C610DE3
    dedust_deposit = 0xB544F4A4

    def __repr__(self):
        return f"{self.value}"

    @classmethod
    def get_random(cls):
        all_ = list(cls)
        return all_[random.randint(0, len(all_) - 1)]

    @classmethod
    def item_list(cls):
        return [opcode.value for opcode in cls]

dedust_url = "https://tonstarter-cdn.ams3.digitaloceanspaces.com/openrating/dedust/dedust.png"
stonfi_icon_url = "https://static.ston.fi/favicon/android-chrome-512x512.png"
parent_task = Task(
    id=-1,
    title="Connect your wallet",
    icon="https://example.com/icon.png",
    description="Connect your wallet to earn 200 XP",
    images=["https://example.com/image1.png"],
    active=True,
    xp=200,
    contract_addresses=[],
    op_code=None,
    min_amount=0,
    parent_id=None,
)

tasks = [
    # Task(
    #     id=2,
    #     title="Deposit TON to your wallet",
    #     icon="https://example.com/icon.png",
    #     description="Deposit TON to your wallet to earn 200 XP",
    #     images=["https://example.com/image1.png"],
    #     active=True,
    #     xp=100,
    #     contract_addresses=[],
    #     op_code=OpCodes.dedust_swap,
    #     min_amount=0,
    #     parent_id=parent_task.id,
    # ),
    Task(
        id=3,
        title="Perform swap",
        icon=dedust_url,
        description="Make dedust swap at any pool to earn 300 XP. "
                    "For example you can use this more safety pool.",
        images=["https://example.com/image1.png"],
        active=True,
        xp=300,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=-1,
        external_url="https://dedust.io/swap/TON/USDT",

),
    Task(
        id=4,
        title="Add liquidity",
        icon=dedust_url,
        description="Complete the fourth task to earn 400 XP",
        images=["https://example.com/image1.png"],
        active=True,
        xp=400,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=3,
        external_url="https://dedust.io/pools/EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r",
),
Task(
        id=5,
        title="Perform swap",
        icon=stonfi_icon_url,
        description="Make dedust swap at any pool to earn 300 XP. "
                    "For example you can use this more safety pool.",
        images=["https://example.com/image1.png"],
        active=False,
        xp=300,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=-1,
        external_url="https://dedust.io/swap/TON/USDT",

),
    Task(
        id=6,
        title="Add liquidity",
        icon=stonfi_icon_url,
        description="Complete the fourth task to earn 400 XP",
        images=["https://example.com/image1.png"],
        active=False,
        xp=400,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=5,
        external_url="https://dedust.io/pools/EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r",
),
]


async def add_tasks():
    await db.create_task(parent_task)
    for task in tasks:
        await db.create_task(task)

async def delete_all_tasks():
    tasks = await db.get_tasks()
    for task in tasks:
        await db.db.tasks.delete_one({"id": task.id})


if __name__ == '__main__':
    import asyncio
    asyncio.run(add_tasks())