from typing import Any

import fastapi

from core.config import base_config
from database.repository import NotFound, CustomMotorClient
from .repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import User, CreateUser, Task, CompleteTask
from pytoniq_core import Address
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

from api_client import scanner_producer


engine = create_async_engine(base_config.database_uri, echo=False)
async_session = async_sessionmaker(
    engine, expire_on_commit=False
)

# db = CustomMotorClient(MONGO_URI)
db = TonQuestSQLAlchemyRepo(async_session)
app_router = fastapi.APIRouter()

@app_router.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    try:
        user = await db.get_user(user_id)
    except NotFound:
        return {"error": "User not found"}
    # user = await db.create_user(user_id)
    return user.dict()

# @app.post("/users/wallet")
# async def create_user_wallet(user_id: int, wallet: str) -> dict:
#     user = await db.get_user(user_id)
#     try:
#         user.address = Address(wallet).to_str(False)
#     except ValueError:
#         return {"error": "Invalid wallet address"}
#     await db.db.users.update_one({"id": user_id}, {"$set": {"address": user.address}})
#     await scanner_producer.add_user_to_track(user.address)
#     await db.complete_task(user.address, None)
#     return user.dict()


@app_router.post("/users/")
async def create_user(user: CreateUser) -> dict:
    try:
        await db.get_user(user.id)
        return {"error": "User already exist"}
    except NotFound:
        pass
    _user = User(**user.dict())
    await db.create_user(_user)
    return user.dict()

@app_router.get("/users/address/{user_id}/{address}")
async def set_user_address(user_id: int, address: str) -> dict:
    user = await db.get_user(user_id)
    if user.address !=  "":
        return {"error": "User already has address"}
    try:
        user.address = Address(address).to_str(False)
    except ValueError:
        return {"error": "Invalid wallet address"}
    await db.db.users.update_one({"id": user_id}, {"$set": {"address": user.address, "xp": 100}})
    await scanner_producer.add_user_to_track(user.address)
    await db.complete_task(user.address, None)
    return user.dict()


@app_router.get("/tasks/{task_id}")
async def get_task(task_id: int) -> Task:
    task = await db.get_task(task_id)
    return task

@app_router.get("/users/task/{task_id}")
async def get_user_task(user_id: int, task_id: int) -> dict:
    user = await db.get_user(user_id)
    completed = False
    if task_id in user.completed_tasks:
        completed = True
    return {"completed": completed}

@app_router.get("/tasks")
async def get_tasks() -> Any:
    tasks = await db.get_all_tasks_by_root()
    result = (await db.build_task_tree(tasks))[0].children
    return [task.dict() for task in result]


@app_router.post("/tasks/")
async def create_task(task: Task) -> dict:
    _task = Task(**task.dict())
    await db.create_task(_task)
    return task.dict()

@app_router.post("/tasks/complete")
async def complete_task(data: CompleteTask) -> dict:
    await db.complete_task(data.address, data.op_code)
    return {"status": "ok"}

@app_router.get("/nfts")
async def get_nfts() -> Any:
    nfts = await db.get_all_nfts()
    return [nft.to_read_model() for nft in nfts]

@app_router.get("/categories")
async def get_categories() -> Any:
    categories = await db.get_all_categories()
    return [category.to_read_model() for category in categories]

# @app.middleware("http")
# async def add_process_time_header(request: fastapi.Request, call_next):
#     try:
#         init_data = request.headers["init-data"]
#         web_app_data = safe_parse_webapp_init_data(init_data)
#         # request.web_app_data = web_app_data
#         response = await call_next(request)
#     except Exception:
#         response = fastapi.Response("Invalid init data", status_code=400)
#     return response

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)