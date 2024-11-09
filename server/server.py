import fastapi
from aiogram.utils.web_app import safe_parse_webapp_init_data
from database import CustomMotorClient
from models import User, Task, CreateUser
from config import MONGO_URI, BOT_TOKEN

db = CustomMotorClient(MONGO_URI)
app = fastapi.FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    user = await db.get_user(user_id)
    # user = await db.create_user(user_id)
    return user.dict()

@app.post("/users/")
async def create_user(user: CreateUser) -> dict:
    _user = User(**user.dict())
    await db.create_user(_user)
    return user.dict()

@app.post("/users/address/{address}")
async def set_user_address(user_id: int, address: str) -> dict:
    user = await db.get_user(user_id)
    user.address = address
    await db.db.users.update_one({"id": user_id}, {"$set": {"address": address}})
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
async def complete_task(address: str, op_code: str) -> dict:
    await db.complete_task(address, op_code)
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
    uvicorn.run(app, host="0.0.0.0", port=8000)