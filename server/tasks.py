from pprint import pprint

from config import MONGO_URI
from database import CustomMotorClient
from models import User, Task

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


parent_task = Task(
    id=1,
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
    Task(
        id=2,
        title="Deposit TON to your wallet",
        icon="https://example.com/icon.png",
        description="Deposit TON to your wallet to earn 200 XP",
        images=["https://example.com/image1.png"],
        active=True,
        xp=100,
        contract_addresses=[],
        op_code=OpCodes.default_message,
        min_amount=0,
        parent_id=parent_task.id,
    ),
    Task(
        id=3,
        title="Make dedust swap at any pool",
        icon="https://example.com/icon.png",
        description="Make dedust swap at any pool to earn 300 XP. "
                    "For example you can use this more safety pool.",
        images=["https://example.com/image1.png"],
        active=True,
        xp=300,
        contract_addresses=[],
        op_code=OpCodes.dedust_swap,
        min_amount=0,
        parent_id=2,
        external_url="https://dedust.io/swap/TON/USDT",

),
    Task(
        id=4,
        title="Make deposit at any pool",
        icon="https://example.com/icon.png",
        description="Complete the fourth task to earn 400 XP",
        images=["https://example.com/image1.png"],
        active=True,
        xp=400,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=2,
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