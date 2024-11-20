from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from database.engine import db

from typing import Any
from database.repository import NotFound
from apps.ton_quest.schemas import User, CreateUser, Task, CompleteTask
from apps.ton_quest import models
from pytoniq_core import Address
from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Security
from apps.ton_quest.web_app_auth import WebAppAuthHeader

db: TonQuestSQLAlchemyRepo

ton_quest_router = APIRouter()

web_app_auth_header = WebAppAuthHeader(name='Authorization', scheme_name='web-app-auth')

@ton_quest_router.get("/login")
async def login(web_app_init_data: WebAppInitData = Security(web_app_auth_header)):

    return web_app_init_data


@ton_quest_router.get("/nfts")
async def get_nfts():
    nfts = await db.get_nfts()
    result = [nft.to_read_model() for nft in nfts]
    return result

@ton_quest_router.get("/nfts/{ntf_id}")
async def get_nft(ntf_id: str) -> dict:
    nft = await db.get_nft(ntf_id)
    return nft


app_router = ton_quest_router
@app_router.get("/users")
async def get_user(web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> dict:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        user = models.User(
            telegram_id=web_app_init_data.user.id,
            username=web_app_init_data.user.username,
            first_name=web_app_init_data.user.first_name,
            last_name=web_app_init_data.user.last_name,
            image=web_app_init_data.user.photo_url
        )
        await db.create_user(user)
    return user.to_read_model()

# @app_router.post("/users/")
# async def create_user(user: CreateUser) -> dict:
#     try:
#         await db.get_user(user.id)
#         return {"error": "User already exist"}
#     except NotFound:
#         pass
#     _user = models.User(**user.dict())
#     await db.create_user(_user)
#     return _user.dict()

@app_router.get("/users/address/{address}")
async def set_user_address(address: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> dict:
    user = await db.get_user(web_app_init_data.user.id)
    if user.wallet_address is not None:
        return {"error": "User already has address"}
    try:
        address = Address(address).to_str(False)
    except ValueError:
        return {"error": "Invalid wallet address"}    
    user = await db.add_user_wallet_address(web_app_init_data.user.id, address)
    # await scanner_producer.add_user_to_track(user.address)
    # await db.complete_task(user.address, None)
    return user.dict()


@app_router.get("/tasks/{task_id}")
async def get_task(task_id: str) -> Task:
    task = await db.get_task(task_id)
    return task

@app_router.get("/task/{task_id}/check")
async def check_task(task_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> dict:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}
    
    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}
    
    completed = await db.check_task_completed(web_app_init_data.user.id, task_id)
    return {'completed': completed}

@app_router.post("/task/{task_id}/claim")
async def claim_task(task_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> dict:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}
    
    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}
    
    completed = await db.check_task_completed(web_app_init_data.user.id, task_id)
    if not completed:
        return {"error": "Task not completed"}
    await db.claim_task(web_app_init_data.user.id, task_id)
    return {"success": True}

@app_router.get("/tasks/{task_id}/complete")
async def complete_task(task_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> bool:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}
    
    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}
    
    try:
        user_task = await db.get_user_task(web_app_init_data.user.id, task_id)
        if user_task.completed:
            return {"error": "Task already completed"}
    except NotFound:
        user_task = await db.create_user_task(web_app_init_data.user.id, task_id)
    
    await db.complete_task(web_app_init_data.user.id, task_id)
    return {"success": True}



@app_router.get("/categories")
async def get_categories() -> Any:
    categories = await db.get_all_categories()
    return [category.to_read_model() for category in categories]

@app_router.get('/categories/{category_id}')
async def get_category(category_id: str) -> Any:
    category = await db.get_category(category_id)
    return category.to_read_model()


@app_router.get('/branches/{branch_id}')
async def get_branch(branch_id: str) -> Any:
    branch = await db.get_branch(branch_id)
    return branch.to_read_model()

@app_router.get('/branches/{branch_id}/check')
async def check_branch(branch_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> bool:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}
    
    try:
        branch = await db.get_branch(branch_id)
    except NotFound:
        return {"error": "Branch not found"}

    completed = await db.check_branch_completed(web_app_init_data.user.id, branch_id)
    return {"completed": completed}


@app_router.get('/branches/{branch_id}/complete')
async def complete_branch(branch_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> Any:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}
    
    try:
        branch = await db.get_branch(branch_id)
    except NotFound:
        return {"error": "Branch not found"}

    try:
        user_branch = await db.get_user_branch(web_app_init_data.user.id, branch_id)
        if user_branch.completed:
            return {"error": "Branch already completed"}
    except NotFound:
        user_branch = await db.create_user_branch(web_app_init_data.user.id, branch_id)
    
    for task in branch.tasks:
        completed = await db.check_task_completed(web_app_init_data.user.id, task.id)
        if not completed:
            return {"error": "Not all tasks in branch completed"}
    await db.complete_branch(web_app_init_data.user.id, branch_id)
    return {"success": True}


@app_router.get('/pieces/{piece_id}/claim')
async def claim_piece(piece_id: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> Any:
    try:
        piece = await db.get_piece(piece_id)
    except NotFound:
        return {"error": "Piece not found"}
    
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        user_piece = await db.get_user_piece(web_app_init_data.user.id, piece_id)
        if user_piece.claimed:
            return {"error": "Piece already claimed"}
    except NotFound:
        user_piece = await db.create_user_piece(web_app_init_data.user.id, piece_id)

    branch_completed = await db.check_branch_completed(web_app_init_data.user.id, piece.branch_id)
    if not branch_completed:
        return {"error": "Branch not completed"}
    
    await db.claim_piece(web_app_init_data.user.id, piece_id)
    return {"success": True}
