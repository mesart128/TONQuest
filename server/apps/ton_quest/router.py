from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from database.engine import db
db: TonQuestSQLAlchemyRepo


from fastapi import APIRouter

nft_router = APIRouter()

@nft_router.get("/nft")
async def get_nft():
    nfts = await db.get_nfts()
    print(nfts)
    return {}