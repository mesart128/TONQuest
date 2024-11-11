import logging

from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Task, ResponseAllTask
from typing import List, Optional


logger = logging.getLogger("uvicorn")

class NotFound(Exception):
    pass


class CustomMotorClient(AsyncIOMotorClient):
    async def get_user(self, user_id: int) -> User:
        user = await self.db.users.find_one({"id": user_id})
        if user is None:
            raise NotFound("User not found")
        return User(**user)
    
    async def create_user(self, user: User) -> User:
        await self.db.users.insert_one(user.dict())
        return user
    
    async def get_tasks(self) -> List[Task]:
        tasks = self.db.tasks.find({})
        tasks = [task async for task in tasks]
        return [Task(**task) for task in tasks]
    
    async def get_task(self, task_id: int) -> Task:
        task = await self.db.tasks.find_one({"task_id": task_id})
        return Task(**task)

    async def get_task_by_op_code(self, op_code: Optional[str]) -> Optional[Task]:
        task = await self.db.tasks.find_one({"op_code": op_code})
        return Task(**task) if task else None
    
    async def get_user_by_address(self, address: str) -> User:
        user = await self.db.users.find_one({"address": address})
        return User(**user) if user else None
    
    async def complete_task(self, address: str, op_code: Optional[str]) -> bool:
        user = await self.get_user_by_address(address)
        if user is None:
            logger.info(f"User with address {address} not found")
            return False
        task = await self.get_task_by_op_code(op_code)
        if not task:
            logger.info(f"Task with op_code {op_code} not found")
            return False
        if task.id not in user.completed_tasks:
            user.completed_tasks.append(task.id)
            await self.db.users.update_one({"address": address}, {"$set": {"completed_tasks": user.completed_tasks,
                                                                           "xp": user.xp + task.xp}})
            logger.info(f"Task {task} completed by user {user}")
            return True
        else:
            logger.info(f"Task {task.id} already completed by user {user.id}")
        return False
    
    async def create_task(self, task: Task) -> Task:
        await self.db.tasks.insert_one(task.dict())
        return task

    async def get_all_tasks_by_root(self) -> List[ResponseAllTask]:
        tasks_data = self.db.tasks.find({})
        tasks = [ResponseAllTask(**task) async for task in tasks_data]
        return tasks

    async def build_task_tree(self, tasks: List[Task]) -> List[Task]:
        task_dict = {task.id: task for task in tasks}
        root_tasks = []

        for task in tasks:
            if task.parent_id is None:
                root_tasks.append(task)
            else:
                parent_task: ResponseAllTask = task_dict.get(task.parent_id)
                if parent_task:
                    parent_task.children.append(task)

        return root_tasks
