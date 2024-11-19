import asyncio

from sqlalchemy import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from apps.ton_quest.enums import TaskTypeEnum
from apps.ton_quest.models import Branch, Category, User, Slide, NFT, Piece, Task
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo  # Замените на реальный путь

DATABASE_URL = "postgresql+asyncpg://creator:creator@localhost/tonquest"  # Укажите свои данные подключения

engine = create_async_engine(DATABASE_URL, echo=True)
SessionFactory = async_sessionmaker(engine)
repo = TonQuestSQLAlchemyRepo(SessionFactory)

async def populate_database():
    async with engine.begin() as conn:
        await conn.run_sync(Branch.metadata.create_all)  # Создание таблиц, если они отсутствуют

    # Категория
    dex_category_data = {
        "head": "DEX",
        "title": "Easy start",
        "description": "You will learn how to use decentralized exchange tools",
        "image": "https://kauri.io/images/1x1.png",
        "subtitle": "This branch focuses on introducing users to Dedust through hands-on tasks, with interactive and easy-to-understand explanations.",
    }
    dex_category_id = await repo.add_one(Category, dex_category_data)
    dedust_branch_data = {
        "title": "Dedust",
        "category_id": dex_category_id,
    }
    dedust_branch_id = await repo.add_one(Branch, dedust_branch_data)

    dedust_first_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Perform a token swap on Dedust",
        "xp": 100,
        "queue": 1,
        "task_type": TaskTypeEnum.dedust_swap,
        "action_url": "https://dedust.io/register",
        "call_to_action": "You have learned how to change one token for another, keep it up!",
    }
    dedust_first_task_id = await repo.add_one(Task, dedust_first_task_data)

    slides_first_task = [
        {
            "task_id": dedust_first_task_id,
            "title": "Introduction to Dedust",
            "description": "Learn the basics of decentralized exchanges.",
            "image": "https://kauri.io/images/slide1.png",
            "queue": 1,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Create a Wallet",
            "description": "Steps to create a wallet for DEX.",
            "image": "https://kauri.io/images/slide2.png",
            "queue": 2,
        },
    ]
    for slide in slides_first_task:
        await repo.add_one(Slide, slide)

    # Вторая задача и слайды
    dedust_second_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Make your first trade",
        "xp": 200,
        "queue": 2,
        "task_type": "dedust_swap",
        "action_url": "https://dedust.io/trade",
        "call_to_action": "Start trading",
    }
    dedust_second_task_id = await repo.add_one(Task, dedust_second_task_data)

    slides_second_task = [
        {
            "task_id": dedust_second_task_id,
            "title": "Trade on Dedust",
            "description": "Learn how to trade on Dedust.",
            "image": "https://kauri.io/images/slide3.png",
            "queue": 1,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Trade on Dedust",
            "description": "Learn how to trade on Dedust.",
            "image": "https://kauri.io/images/slide4.png",
            "queue": 2,
        },
    ]
    for slide in slides_second_task:
        await repo.add_one(Slide, slide)

    # Пользователь
    test_user_data = {
        "telegram_id": 12345678,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "image": "https://kauri.io/images/user.png",
        "wallet_address": "0x123456789abcdef",
    }
    test_user_id = await repo.add_one(User, test_user_data)

    # NFT и части
    test_nft_data = {
        "image": "https://kauri.io/images/nft.png",
        "contract_address": "0xabcdef123456789",
    }
    test_nft_id = await repo.add_one(NFT, test_nft_data)

    pieces = [
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece1.png"},
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece2.png"},
    ]
    for piece in pieces:
        await repo.add_one(Piece, piece)

    print("Database population completed.")

# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(populate_database())
