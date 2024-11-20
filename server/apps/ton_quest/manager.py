import logging

from pydantic import BaseModel

from apps.ton_quest.models import User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import DedustEvent
from database.engine import db

db: TonQuestSQLAlchemyRepo


async def check_task(user_account: User, task_type: BaseModel) -> bool:
    if isinstance(task_type, DedustEvent):
        task = await db.get_task_by_task_type(task_type=task_type.event_type)
        if task is None:
            logging.warning(f"Task {task_type.event_type} not found. {user_account}")
            return
        branch = await db.get_branch(task.branch_id)

    return False
