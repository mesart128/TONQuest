from fastapi import APIRouter

from apps.account.router import account_router
from apps.scanner.router import scanner_router
from apps.ton_quest.router import ton_quest_router

v1_router = APIRouter()

v1_router.include_router(ton_quest_router)
v1_router.include_router(account_router)
v1_router.include_router(scanner_router)


@v1_router.get("/")
async def root():
    return {"message": "Hello World"}
