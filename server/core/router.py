from fastapi import APIRouter

from server.apps.account.router import account_router
from server.apps.scanner.router import scanner_router

v1_router = APIRouter()

v1_router.include_router(account_router)
v1_router.include_router(scanner_router)


@v1_router.get("/")
async def root():
    return {"message": "Hello World"}
