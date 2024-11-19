from apps.ton_quest.tasks import OpCodes
from typing import Optional
import pydantic

class Task(pydantic.BaseModel):
    id: int
    title: str
    icon: str
    description: str
    images: list
    active: bool
    xp: int
    contract_addresses: list
    op_code: Optional[str] = None
    min_amount: float
    parent_id: int | None = None
    external_url: Optional[str] = None
    children: list = []

def reformat_tasks(tasks):
    task_dict = {task.id: task for task in tasks}
    root_tasks = []
    parent_id = 0
    for task in tasks:
        if task.parent_id == parent_id:
            root_tasks.append(task)
        else:
            parent_task = task_dict.get(task.parent_id)
            if parent_task:
                parent_task.children.append(task)

    return root_tasks

# Example usage
tasks = [
    Task(
        id=2,
        title="Deposit TON",
        icon="https://cryptologos.cc/logos/toncoin-ton-logo.png",
        description="Deposit TON to your wallet to earn 200 XP",
        images=["https://example.com/image1.png"],
        active=True,
        xp=50,
        contract_addresses=[],
        op_code=OpCodes.default_message,
        min_amount=0,
        parent_id=0,
        external_url="https://example.com"
    ),
    Task(
        id=3,
        title="Perform a swap",
        icon="https://tonstarter-cdn.ams3.digitaloceanspaces.com/openrating/dedust/dedust.png",
        description="Make dedust swap at any pool to earn 300 XP. "
                    "For example you can use this more safety pool.",
        images=["https://example.com/image1.png"],
        active=True,
        xp=50,
        contract_addresses=[],
        op_code=OpCodes.dedust_swap,
        min_amount=0,
        parent_id=2,
        external_url="https://dedust.io/swap/TON/USDT"
    ),
    Task(
        id=4,
        title="Add liquidity",
        icon="https://tonstarter-cdn.ams3.digitaloceanspaces.com/openrating/dedust/dedust.png",
        description="Complete the fourth task to earn 400 XP",
        images=["https://example.com/image1.png"],
        active=True,
        xp=150,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=3,
        external_url="https://dedust.io/pools/EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r"
    ),
    Task(
        id=5,
        title="Perform swap",
        icon="https://static.ston.fi/favicon/android-chrome-512x512.png",
        description="Complete the fourth task to earn 400 XP",
        images=["https://example.com/image1.png"],
        active=False,
        xp=150,
        contract_addresses=[],
        op_code=OpCodes.dedust_deposit,
        min_amount=0,
        parent_id=2,
        external_url="https://dedust.io/pools/EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r"
    ),
]

reformatted_tasks = reformat_tasks(tasks)
print(reformatted_tasks)