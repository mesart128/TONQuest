from typing import Any, List, Union
from uuid import UUID

from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Security
from pytoniq_core import Address

from apps.ton_quest import models, schemas
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.web_app_auth import WebAppAuthHeader
from apps.transaction.schemas import TaskResponse
from database.engine import db
from database.repository import NotFound

db: TonQuestSQLAlchemyRepo

ton_quest_router = APIRouter()

web_app_auth_header = WebAppAuthHeader(name="Authorization", scheme_name="web-app-auth")


@ton_quest_router.get("/login")
async def login(web_app_init_data: WebAppInitData = Security(web_app_auth_header)):
    return web_app_init_data


@ton_quest_router.get("/users")
async def get_user(web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> schemas.User:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        user = models.User(
            telegram_id=web_app_init_data.user.id,
            username=web_app_init_data.user.username,
            first_name=web_app_init_data.user.first_name,
            last_name=web_app_init_data.user.last_name,
            image=web_app_init_data.user.photo_url,
        )
        user = await db.create_user(user)
    return schemas.User(**user.to_read_model())

@ton_quest_router.get("/users/address/{address}")
async def set_user_address(
    address: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> schemas.User:
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
    return schemas.User(**user.to_read_model())


@ton_quest_router.get(
    "/tasks/{task_id}",
)
async def get_task(task_id: UUID) -> schemas.Task:
    task = await db.get_task_with_slides(task_id)
    return schemas.Task(**task.to_read_model())


@ton_quest_router.get("/task/{task_id}/check")
async def check_task(
    task_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.IsCompletedResponse, schemas.ErrorResponse]:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}

    completed = await db.check_task_completed(user.id, task_id)
    return {"completed": completed}


@ton_quest_router.post("/task/{task_id}/claim")
async def claim_task(
    task_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.SuccessResponse, schemas.ErrorResponse]:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}

    completed = await db.check_task_completed(user.id, task_id)
    if not completed:
        return {"error": "Task not completed"}
    await db.claim_task(web_app_init_data.user.id, task_id)
    return {"success": True}


@ton_quest_router.get("/tasks/{task_id}/complete")
async def complete_task(
    task_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.SuccessResponse, schemas.ErrorResponse]:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        task = await db.get_task(task_id)
    except NotFound:
        return {"error": "Task not found"}
    
    branch_tasks = (await db.get_branch(task.branch_id)).tasks
    for branch_task in branch_tasks:
        if branch_task.queue < task.queue:
            completed = await db.check_task_completed(user.id, branch_task.id)
            if not completed:
                return {"error": "Previous task not completed"}

    try:
        user_task = await db.get_user_task(user.id, task_id)
        if user_task.completed:
            return {"error": "Task already completed"}
    except NotFound:
        user_task = await db.create_user_task(user.id, task_id)

    await db.complete_task(user.id, task_id)
    return {"success": True}


@ton_quest_router.get("/categories")
async def get_categories() -> List[schemas.Category]:
    categories = await db.get_all_categories()
    return [schemas.Category(**category.to_read_model()) for category in categories]


@ton_quest_router.get("/categories/{category_id}")
async def get_category(category_id: UUID) -> schemas.Category:
    category = await db.get_category(category_id)
    return schemas.Category(**category.to_read_model())


@ton_quest_router.get("/branches/{branch_id}")
async def get_branch(branch_id: UUID) -> schemas.Branch:
    branch = await db.get_branch(branch_id)
    return schemas.Branch(**branch.to_read_model())


@ton_quest_router.get("/branches/{branch_id}/check")
async def check_branch(
    branch_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.IsCompletedResponse, schemas.ErrorResponse]:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        branch = await db.get_branch(branch_id)
    except NotFound:
        return {"error": "Branch not found"}

    completed = await db.check_branch_completed(user.id, branch_id)
    return {"completed": completed}


@ton_quest_router.get("/branches/{branch_id}/complete")
async def complete_branch(
    branch_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.SuccessResponse, schemas.ErrorResponse]:
    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        branch = await db.get_branch(branch_id)
    except NotFound:
        return {"error": "Branch not found"}

    try:
        user_branch = await db.get_user_branch(user.id, branch_id)
        if user_branch.completed:
            return {"error": "Branch already completed"}
    except NotFound:
        user_branch = await db.create_user_branch(user.id, branch_id)

    for task in branch.tasks:
        completed = await db.check_task_completed(user.id, task.id)
        if not completed:
            return {"error": "Not all tasks in branch completed"}
    await db.complete_branch(user.id, branch_id)
    return {"success": True}


@ton_quest_router.get("/nfts")
async def get_nfts() -> List[schemas.NFT]:
    nfts = await db.get_nfts()
    return [schemas.NFT(**nft.to_read_model()) for nft in nfts]

@ton_quest_router.get("/nfts/{ntf_id}")
async def get_nft(ntf_id: UUID) -> schemas.NFT:
    nft = await db.get_nft(ntf_id)
    return schemas.NFT(**nft.to_read_model())


@ton_quest_router.get("/pieces/{piece_id}/claim")
async def claim_piece(
    piece_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> Union[schemas.SuccessResponse, schemas.ErrorResponse]:
    try:
        piece = await db.get_piece(piece_id)
    except NotFound:
        return {"error": "Piece not found"}

    try:
        user = await db.get_user(web_app_init_data.user.id)
    except NotFound:
        return {"error": "User not found"}

    try:
        user_piece = await db.get_user_piece(user.id, piece_id)
        if user_piece.claimed:
            return {"error": "Piece already claimed"}
    except NotFound:
        await db.create_user_piece(user.id, piece_id)

    branch_completed = await db.check_branch_completed(user.id, piece.branch_id)
    if not branch_completed:
        return {"error": "Branch not completed"}

    await db.claim_piece(user.id, piece_id)
    return {"success": True}
