import logging
from typing import List, Optional, Union
from uuid import UUID

from aiogram.utils.web_app import (
    WebAppInitData,
    parse_webapp_init_data,
)
from fastapi import APIRouter, HTTPException, Request, Security
from pytoniq_core import Address

from apps.ton_quest import models, schemas
from apps.ton_quest.enums import TaskStatusEnum, TaskTypeEnum
from apps.ton_quest.models import Branch, Piece
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.web_app_auth import WebAppAuthHeader
from database import initial_data
from database.engine import db, engine
from database.initial_data import populate_database
from database.repository import NotFound

db: TonQuestSQLAlchemyRepo


class CustomWebAppAuthHeader(WebAppAuthHeader):
    async def __call__(self, request: Request) -> Optional[WebAppInitData]:
        init_data = request.headers.get(self.model.name)
        if not init_data:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                return None

        parsed_init_data = parse_webapp_init_data(init_data)
        return parsed_init_data


web_app_auth_header = CustomWebAppAuthHeader(name="Authorization", scheme_name="web-app-auth")

ton_quest_router = APIRouter()


async def calculate_user_xp(user: models.User, db_: TonQuestSQLAlchemyRepo) -> int:
    xp = 0
    for task_id in user.completed_tasks:
        task = await db_.get_task(task_id.task_id)
        xp += task.xp
    return xp


@ton_quest_router.get("/login")
async def login(web_app_init_data: WebAppInitData = Security(web_app_auth_header)):
    await initial_data.populate_database(engine, db)
    return web_app_init_data


@ton_quest_router.get("/users")
async def get_user(
    web_app_init_data: WebAppInitData = Security(web_app_auth_header),
) -> schemas.User:
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
    response_dict = user.to_read_model()
    response_dict['wallet_address'] = Address(response_dict['wallet_address']).to_str() if response_dict['wallet_address'] else None
    response_dict["xp"] = await calculate_user_xp(user, db)
    return schemas.User(**response_dict)


# @ton_quest_router.get("/users/{address}/")
# async def get_completed_user(address: str) -> List[schemas.Task]:
#     try:
#         user = await db.get_user_by(wallet_address=Address(address).to_str(False))
#     except NotFound:
#         raise HTTPException(status_code=404, detail="User not found")
#     result = [(await db.get_task(task.task_id)).to_read_model() for task in user.completed_tasks]
#     return result


@ton_quest_router.get("/users/address/{address}")
async def set_user_address(
    address: str, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> schemas.User | dict:
    user = await db.get_user(web_app_init_data.user.id)
    if user.wallet_address is not None:
        return {"error": "User already has address"}
    try:
        address = Address(address).to_str(False)
    except ValueError:
        return {"error": "Invalid wallet address"}
    user_ = await db.add_user_wallet_address(user.id, address)
    wallet_task = await db.get_tasks_by_task_type(TaskTypeEnum.connect_wallet)
    for task in wallet_task:
        await db.create_user_task(user_.id, task.id, completed=True)
    updated_user = await db.get_user_by(id=user_.id)
    response = updated_user.to_read_model()
    response['wallet_address'] = Address(response['wallet_address']).to_str()
    response["xp"] = await calculate_user_xp(updated_user, db)
    return schemas.User(**response)


@ton_quest_router.get(
    "/tasks/{task_id}",
)
async def get_task(task_id: UUID) -> schemas.Task:
    task = await db.get_task_with_slides(str(task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
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
    await db.claim_task(user.id, task_id)
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


def calculate_category_xp(category):
    xp = 0
    for branch in category.branches:
        for task in branch.tasks:
            xp += task.xp
    return xp


@ton_quest_router.get("/categories")
async def get_categories() -> List[schemas.Category]:
    categories = await db.get_all_categories()
    result_list = []
    for category in categories:
        dict_to_return = category.to_read_model()
        dict_to_return["xp"] = calculate_category_xp(category)
        result_list.append(dict_to_return)
    return [schemas.Category(**category) for category in result_list]


@ton_quest_router.get("/categories/{category_id}")
async def get_category(category_id: UUID) -> schemas.Category:
    category = await db.get_category(category_id)
    return schemas.Category(**category.to_read_model())


@ton_quest_router.get("/branches/{branch_id}")
async def get_branch(
    branch_id: UUID, web_app_init_data: WebAppInitData = Security(web_app_auth_header)
) -> schemas.UserBranch:
    user = await db.get_user(web_app_init_data.user.id)
    branch = await db.get_branch(str(branch_id))
    branch.tasks.sort(key=lambda task_: task_.queue)
    active_task_found = False
    tasks_with_status = []
    claimed_tasks_ids = [task.task_id for task in user.claimed_tasks]
    for task in branch.tasks:
        if task.id in claimed_tasks_ids:
            status = TaskStatusEnum.claimed
        elif not active_task_found:
            status = TaskStatusEnum.active
            active_task_found = True
        else:
            status = TaskStatusEnum.blocked
        task_read_model = task.to_read_model()
        task_read_model["status"] = status
        tasks_with_status.append(task_read_model)
    branch_read_model = branch.to_read_model()
    branch_read_model["tasks"] = tasks_with_status
    return schemas.UserBranch(**branch_read_model)


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
        logging.error(f"User {user.id} not found in branch {branch_id}")
        user_branch = await db.create_user_branch(user.id, branch_id)
        logging.debug(f"User {user.id} added to branch {branch_id}")

    for task in branch.tasks:
        completed = await db.check_task_completed(user.id, task.id)
        if not completed:
            return {"error": "Not all tasks in branch completed"}
    updated_branch = await db.complete_branch(user.id, branch_id)
    logging.debug(f"Branch {branch_id} completed. {updated_branch}")
    return {"success": True}


@ton_quest_router.get("/nft")
async def get_nfts(web_app_init_data: WebAppInitData = Security(web_app_auth_header)) -> dict:
    nfts = await db.get_nfts()
    if not nfts:
        raise HTTPException(status_code=404, detail="NFTs not found")
    first_nft = nfts[0]
    pieces = first_nft.pieces
    user = await db.get_user(web_app_init_data.user.id)
    tasks = []
    for piece in pieces:
        piece: Piece
        result = {}
        branch: Branch = await db.get_branch(piece.branch_id)
        result["card"] = {
            "title": branch.title,
            # "is_completed": await db.check_branch_completed(user.id, branch.id),
            "received": branch.id in [branch.branch_id for branch in user.completed_branches],
            "subtasks": [
                {"subtaskId": task.queue, "isCompleted": await db.check_task_completed(user.id, task.id)} for task in branch.tasks
            ]
        }
        tasks.append(result)
    return {"nft": [nft.to_read_model() for nft in nfts], "cards": tasks}

    # return schemas.NFT(**first_nft.to_read_model())


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


@ton_quest_router.get("/reset_database")
async def reset_database():
    await populate_database(engine, db)
    return {"success": True}
