from core.router import v1_router

@v1_router.get("/nft")
async def get_nft():
    return {"message": "Hello NFT"}