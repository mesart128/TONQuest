import logging

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from aiogram.utils.web_app import safe_parse_webapp_init_data

from database import CustomMotorClient, NotFound
from models import User, Task, CreateUser, CompleteTask
from config import MONGO_URI, BOT_TOKEN
from pytoniq_core import Address

from api_client import scanner_producer

db = CustomMotorClient(MONGO_URI)
app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("uvicorn")


@app.get("/users/{user_id}")
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


@app.post("/users/")
async def create_user(user: CreateUser) -> dict:
    try:
        await db.get_user(user.id)
        return {"error": "User already exist"}
    except NotFound:
        pass
    _user = User(**user.dict())
    await db.create_user(_user)
    return user.dict()

@app.post("/users/address/")
async def set_user_address(user_id: int, address: str) -> dict:
    user = await db.get_user(user_id)
    try:
        user.address = Address(address).to_str(False)
    except ValueError:
        return {"error": "Invalid wallet address"}
    await db.db.users.update_one({"id": user_id}, {"$set": {"address": user.address}})
    await scanner_producer.add_user_to_track(user.address)
    await db.complete_task(user.address, None)
    return user.dict()


@app.get("/tasks/{task_id}")
async def get_task(task_id: int) -> Task:
    task = await db.get_task(task_id)
    return task

@app.get("/users/task/{task_id}")
async def get_user_task(user_id: int, task_id: int) -> dict:
    user = await db.get_user(user_id)
    completed = False
    if task_id in user.completed_tasks:
        completed = True
    return {"completed": completed}

@app.get("/tasks")
async def get_tasks() -> list:
    tasks = await db.get_tasks()
    return [task.dict() for task in tasks]
    

@app.post("/tasks/")
async def create_task(task: Task) -> dict:
    _task = Task(**task.dict())
    await db.create_task(_task)
    return task.dict()

@app.post("/tasks/complete")
async def complete_task(data: CompleteTask) -> dict:
    await db.complete_task(data.address, data.op_code)
    return {"status": "ok"}

@app.get("/tasks/random")
async def generate_default_tasks() -> dict:
    from tasks import parent_task, tasks
    await db.create_task(parent_task)
    for task in tasks:
        await db.create_task(task)
    return {"status": "ok"}


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)