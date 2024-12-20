import logging
from typing import List

from apps.ton_quest.models import Task, User, UserTask
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from database.engine import db

db: TonQuestSQLAlchemyRepo


async def complete_task(user_account: User, task: Task) -> bool:
    await db.complete_task(user_account.id, task.id)


async def check_task(user_account: User, event_type: str) -> bool:
    logging.debug(f"Checking task for user {user_account.wallet_address}")
    tasks: List[Task] = await db.get_tasks_by_task_type(task_type=event_type)

    if not tasks:
        logging.warning(f"Tasks {event_type} not found. {user_account}")
        return False

    tasks = sorted(tasks, key=lambda x: x.queue)
    current_task = None
    for task in tasks:
        completed = await db.check_task_completed(user_account.id, task.id)
        logging.debug(f"Checking task {task.queue} for user {user_account}. Completed: {completed}")
        if not completed:
            current_task = task
            break
    if current_task is None:
        logging.debug(f"No tasks found for user {user_account.wallet_address}")
        return False

    branch_tasks = (await db.get_branch(current_task.branch_id)).tasks
    for branch_task in branch_tasks:
        if branch_task.queue < current_task.queue:
            completed = await db.check_task_completed(user_account.id, branch_task.id)
            logging.debug(
                f"Checking branch task {branch_task.queue} "
                f"for user {user_account}. Completed: {completed}"
            )
            if not completed:
                logging.warning(f"Previous task {branch_task.queue} not completed. {user_account}")
                return False
    updated_task: UserTask = await db.complete_task(user_account.id, current_task.id)
    logging.debug(
        f"Task {current_task.queue} completed for user {user_account.wallet_address}. "
        f"{updated_task=}"
    )

    return False
