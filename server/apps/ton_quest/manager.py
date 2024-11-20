import logging

from pydantic import BaseModel

from apps.ton_quest.models import User, Task
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import DedustSwapEvent
from database.engine import db

db: TonQuestSQLAlchemyRepo


async def complete_task(user_account: User, task: Task) -> bool:
    await db.complete_task(user_account.id, task.id)


async def check_task(user_account: User, event_type: BaseModel) -> bool:
    logging.debug(f"Checking task for user {user_account}")
    if isinstance(event_type, DedustSwapEvent):
        task: Task = await db.get_task_by_task_type(task_type=event_type.event_type)
        if task is None:
            logging.warning(f"Task {event_type.event_type} not found. {user_account}")
            return

        logging.debug(f"Checking task {task.id} for user {user_account.id}")
        completed_task = await db.check_task_completed(user_account.id, task.id)
        if completed_task:
            logging.debug(f"Task {task.id} already completed. {user_account}")
            return

        branch = await db.get_branch(task.branch_id)
        if branch is None:
            logging.warning(f"Branch {task.branch_id} not found. {user_account}")
            return
        task_queue = task.queue
        if task_queue <= 1:
            logging.debug(f"Complete {task.id} by. {user_account}")
            await complete_task(user_account, task)
            return True
        else:
            prev_task: Task = await db.get_task_by(queue=task_queue - 1, branch_id=branch.id)
            if prev_task is None:
                logging.error(f"Previous task {task_queue - 1} not found. {user_account}")
                return False
            is_completed_prev_task = await db.check_task_completed(user_id=user_account.id, task_id=prev_task.id)
            if not is_completed_prev_task:
                logging.warning(f"Previous task {prev_task.id} not completed. {user_account}")
                return False
            logging.debug(f"Complete {task.id} by. {user_account}")
            await complete_task(user_account, task)
            return True
    return False
