import logging

from pydantic import BaseModel

from apps.ton_quest.models import User, Task, UserTask
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import DedustSwapEvent, DedustWithdrawEvent, DedustDepositEvent
from database.engine import db

db: TonQuestSQLAlchemyRepo


async def complete_task(user_account: User, task: Task) -> bool:
    await db.complete_task(user_account.id, task.id)


async def check_task(user_account: User, event_type: str) -> bool:
    logging.debug(f"Checking task for user {user_account.wallet_address}")
    task: Task = await db.get_task_by_task_type(task_type=event_type)
    if task is None:
        logging.warning(f"Task {event_type} not found. {user_account}")
        return False
    branch_tasks = (await db.get_branch(task.branch_id)).tasks
    for branch_task in branch_tasks:
        if branch_task.queue < task.queue:
            completed = await db.check_task_completed(user_account.id, branch_task.id)
            logging.debug(f"Checking branch task {branch_task.queue} for user {user_account}. Completed: {completed}")
            if not completed:
                logging.warning(f"Previous task {branch_task.queue} not completed. {user_account}")
                return False
    updated_task: UserTask = await db.complete_task(user_account.id, task.id)
    logging.debug(f"Task {task.queue} completed for user {user_account.wallet_address}. "
                  f"{updated_task=}")

    return False
