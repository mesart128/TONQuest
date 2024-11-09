from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Task
from typing import List


class CustomMotorClient(AsyncIOMotorClient):
    async def get_user(self, user_id: int) -> User:
        user = await self.db.users.find_one({"id": user_id})
        if user is None:
            raise Exception("User not found")
        return User(**user)
    
    async def create_user(self, user: User) -> User:
        await self.db.users.insert_one(user.dict())
        return user
    
    async def get_tasks(self) -> List[Task]:
        tasks = self.db.tasks.find({})
        print(tasks)
        return [Task(**task) async for task in tasks]
    
    async def get_task(self, task_id: int) -> Task:
        task = await self.db.tasks.find_one({"task_id": task_id})
        return Task(**task)

    async def get_task_by_op_code(self, op_code: str) -> Task:
        task = await self.db.tasks.find_one({"op_code": op_code})
        return Task(**task)
    
    async def get_user_by_address(self, address: str) -> User:
        user = await self.db.users.find_one({"address": address})
        return User(**user)
    
    async def complete_task(self, address: str, op_code: str) -> bool:
        user = await self.get_user_by_address(address)
        task = await self.get_task_by_op_code(op_code)
        if task.task_id not in user.completed_tasks:
            user.completed_tasks.append(task.task_id)
            await self.db.users.update_one({"address": address}, {"$set": {"completed_tasks": user.completed_tasks}})
        return True
    
    async def create_task(self, task: Task) -> Task:
        await self.db.tasks.insert_one(task.dict())
        return task

