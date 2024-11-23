from fastapi import APIRouter
from starlette.responses import RedirectResponse

from apps.ton_quest.router import ton_quest_router
from core.config import base_config

v1_router = APIRouter()
# v1_router.mount("/quest", ton_quest_router)


v1_router.include_router(ton_quest_router, include_in_schema=base_config.debug)
# v1_router.include_router(account_router)
# v1_router.include_router(scanner_router)


@v1_router.get("/")
async def root():
    return {"message": "Hello World"}


@v1_router.get("/tonquest-pitch")
async def preview():
    url = base_config.preview_url
    return RedirectResponse(url=url)
