import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.ton_quest.enums import TaskTypeEnum
from apps.ton_quest.models import NFT, Branch, Category, Piece, Slide, Task, User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo  # Замените на реальный путь
from database.base import Base

DATABASE_URL = (
    "postgresql+asyncpg://creator:creator@localhost/tonquest"  # Укажите свои данные подключения
)


async def populate_database(engine, repo):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Создание таблиц, если они отсутствуют
        await conn.run_sync(Base.metadata.create_all)  # Создание таблиц, если они отсутствуют
    # return
    #
    category_connect_wallet_data = {
        "title": "Connect Wallet",
        "head": "Getting Started",
        "description": "Learn how to connect your wallet to the TON ecosystem",
        "image": "https://kauri.io/images/1x1.png",
        "subtitle": "This branch introduces users to the TON ecosystem by explaining how to connect their wallet.",
    }
    connect_wallet_category_id = await repo.add_one(Category, category_connect_wallet_data)

    connect_wallet_branch_data = {
        "title": "Connect Wallet",
        "category_id": connect_wallet_category_id,
    }
    connect_wallet_branch_id = await repo.add_one(Branch, connect_wallet_branch_data)

    connect_wallet_task = {
        "title": "Connect your wallet",
        "xp": 20,
        "queue": 0,
        "task_type": TaskTypeEnum.connect_wallet,
        "action_url": "https://tonos-se.org/",
        "call_to_action": "You have connected your wallet. Great job! "
                          "You've been rewarded by piece of NFT. Keep it up!",
        "branch_id": connect_wallet_branch_id,
    }

    connect_wallet_task_id = await repo.add_one(Task, connect_wallet_task)

    # DEX
    dex_category_data = {
        "head": "DEX",
        "title": "Easy start",
        "description": "You will learn how to use decentralized exchange tools",
        "image": "https://kauri.io/images/1x1.png",
        "subtitle": "This branch focuses on introducing users"
        " to Dedust through hands-on tasks, with interactive and easy-to-understand explanations.",
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
            "title": "Task description",
            "description": "Token swaps allow you to exchange one asset for another. For example, you can swap TON for USDT to secure your assets' value or use the tokens in other DeFi operations.",
            "image": "https://kauri.io/images/slide1.png",
            "queue": 1,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Fiat Analogy",
            "description": "Swapping tokens is like exchanging dollars for euros — you're preparing to use the right 'currency' for your plans, whether it's participating in a new DeFi project or making transactions on a specific platform.",
            "image": "https://kauri.io/images/slide2.png",
            "queue": 2,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Fiat Analogy",
            "description": "Swapping tokens is like exchanging dollars for euros — you're preparing to use the right 'currency' for your plans, whether it's participating in a new DeFi project or making transactions on a specific platform.",
            "image": "https://kauri.io/images/slide2.png",
            "queue": 2,
        },
    ]
    for slide in slides_first_task:
        await repo.add_one(Slide, slide)

    dedust_second_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Provide liquidity on Dedust",
        "xp": 200,
        "queue": 3,
        "task_type": TaskTypeEnum.dedust_liquidity,
        "action_url": "https://dedust.io/trade",
        "call_to_action": "You have learned how to provide liquidity and earn rewards, keep it up!",
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

    dedust_third_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Withdraw liquidity on Dedust",
        "xp": 300,
        "queue": 3,
        "task_type": TaskTypeEnum.dedust_withdraw,
        "action_url": "https://dedust.io/trade",
        "call_to_action": "You have learned how to withdraw liquidity and reclaim the tokens you added to the pool. ",
    }
    dedust_third_task_id = await repo.add_one(Task, dedust_third_task_data)

    slides_third_task = [
        {
            "task_id": dedust_third_task_id,
            "title": "Trade on Dedust",
            "description": "Learn how to trade on Dedust.",
            "image": "https://kauri.io/images/slide3.png",
            "queue": 1,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Trade on Dedust",
            "description": "Learn how to trade on Dedust.",
            "image": "https://kauri.io/images/slide4.png",
            "queue": 2,
        },
    ]
    for slide in slides_third_task:
        await repo.add_one(Slide, slide)

    # EVAA
    evaa_category_data = {
        "head": "Lending & Borrowing",
        "title": "Intro to EVAA",
        "description": "You will learn how to use EVAA lending and borrowing tools in the TON ecosystem.",
        "image": "https://kauri.io/images/1x1.png",
        "subtitle": (
            "This branch introduces users to the mechanisms of borrowing and lending on TON "
            "using EVAA with hands-on tasks and simple, interactive explanations."
        ),
    }
    evaa_category_id = await repo.add_one(Category, evaa_category_data)

    evaa_branch_data = {
        "title": "EVAA Lending & Borrowing",
        "category_id": evaa_category_id,
    }
    evaa_branch_id = await repo.add_one(Branch, evaa_branch_data)

    # Task 1: Supplying
    evaa_first_task_data = {
        "branch_id": evaa_branch_id,
        "title": "Supply Assets on EVAA",
        "xp": 100,
        "queue": 1,
        "task_type": TaskTypeEnum.evaa_supply,
        "action_url": "https://evaa.finance/supply",
        "call_to_action": "You have learned how to supply assets to EVAA and earn interest. Great work!",
    }
    evaa_first_task_id = await repo.add_one(Task, evaa_first_task_data)

    slides_first_task = [
        {
            "task_id": evaa_first_task_id,
            "title": "What is Supplying?",
            "description": (
                "Supplying assets means depositing your tokens into the EVAA protocol. "
                "In return, you earn interest on your assets while they are used by others."
            ),
            "image": "https://kauri.io/images/slide1.png",
            "queue": 1,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Supplying is like putting your money in a savings account. While your money is in the bank, "
                "it earns interest because the bank lends it to others or invests it."
            ),
            "image": "https://kauri.io/images/slide2.png",
            "queue": 2,
        },
    ]
    for slide in slides_first_task:
        await repo.add_one(Slide, slide)

    # Task 2: Borrowing
    evaa_second_task_data = {
        "branch_id": evaa_branch_id,
        "title": "Borrow Assets on EVAA",
        "xp": 200,
        "queue": 2,
        "task_type": TaskTypeEnum.evaa_borrow,
        "action_url": "https://evaa.finance/borrow",
        "call_to_action": "You have learned how to borrow assets on EVAA. Keep up the good work!",
    }
    evaa_second_task_id = await repo.add_one(Task, evaa_second_task_data)

    slides_second_task = [
        {
            "task_id": evaa_second_task_id,
            "title": "What is Borrowing?",
            "description": (
                "Borrowing on EVAA allows you to access liquidity without selling your tokens. "
                "You can use your supplied assets as collateral to secure the loan."
            ),
            "image": "https://kauri.io/images/slide3.png",
            "queue": 1,
        },
        {
            "task_id": evaa_second_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Borrowing is like taking a loan from a bank with your house as collateral. "
                "If you don’t repay the loan, the bank can claim your house."
            ),
            "image": "https://kauri.io/images/slide4.png",
            "queue": 2,
        },
    ]
    for slide in slides_second_task:
        await repo.add_one(Slide, slide)

    # Task 3: Repaying
    evaa_third_task_data = {
        "branch_id": evaa_branch_id,
        "title": "Repay Loans on EVAA",
        "xp": 300,
        "queue": 3,
        "task_type": TaskTypeEnum.evaa_borrow,
        "action_url": "https://evaa.finance/repay",
        "call_to_action": "You have successfully repaid your loan and reclaimed your collateral. Excellent work!",
    }
    evaa_third_task_id = await repo.add_one(Task, evaa_third_task_data)

    slides_third_task = [
        {
            "task_id": evaa_third_task_id,
            "title": "What is Repaying?",
            "description": (
                "Repaying a loan means returning the borrowed assets along with any accrued interest. "
                "Once repaid, your collateral is unlocked."
            ),
            "image": "https://kauri.io/images/slide5.png",
            "queue": 1,
        },
        {
            "task_id": evaa_third_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Repaying a loan is like settling a mortgage. Once you pay it off, "
                "your house (collateral) is fully yours again."
            ),
            "image": "https://kauri.io/images/slide6.png",
            "queue": 2,
        },
    ]
    for slide in slides_third_task:
        await repo.add_one(Slide, slide)


    # TONSTAKERS
    staking_category_data = {
        "head": "Staking",
        "title": "Passive Income",
        "description": "Learn how to stake TON for passive income and maximize your returns.",
        "image": "https://kauri.io/images/1x1.png",
        "subtitle": (
            "This branch introduces users to the staking process, comparing staking pools, "
            "and managing their staked assets for maximum efficiency."
        ),
    }
    staking_category_id = await repo.add_one(Category, staking_category_data)

    staking_branch_data = {
        "title": "Staking (Passive Income)",
        "category_id": staking_category_id,
    }
    staking_branch_id = await repo.add_one(Branch, staking_branch_data)

    # Task 1: Stake TON
    staking_first_task_data = {
        "branch_id": staking_branch_id,
        "title": "Stake TON on BeMo",
        "xp": 100,
        "queue": 1,
        "task_type": TaskTypeEnum.tonstakers_stake,
        "action_url": "https://bemo.fi/",
        "call_to_action": "You’ve successfully staked TON on BeMo. Great job starting your journey to passive income!",
    }
    staking_first_task_id = await repo.add_one(Task, staking_first_task_data)

    slides_first_task = [
        {
            "task_id": staking_first_task_id,
            "title": "What is Staking?",
            "description": (
                "Staking allows you to earn rewards by locking your tokens to support the network's operations. "
                "It’s like earning interest on a fixed deposit."
            ),
            "image": "https://kauri.io/images/slide1.png",
            "queue": 1,
        },
        {
            "task_id": staking_first_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Staking is like depositing money in a high-yield savings account. "
                "The longer you stake, the more rewards you earn."
            ),
            "image": "https://kauri.io/images/slide2.png",
            "queue": 2,
        },
    ]
    for slide in slides_first_task:
        await repo.add_one(Slide, slide)

    # Task 2: Compare Staking Pools
    staking_second_task_data = {
        "branch_id": staking_branch_id,
        "title": "Unstake ",
        "xp": 200,
        "queue": 2,
        "task_type": TaskTypeEnum.tonstakers_unstake,
        "action_url": "https://bemo.fi/",
        "call_to_action": "You’ve learned how to choose the best staking pool. Keep optimizing your rewards!",
    }
    staking_second_task_id = await repo.add_one(Task, staking_second_task_data)

    slides_second_task = [
        {
            "task_id": staking_second_task_id,
            "title": "Why Compare Pools?",
            "description": (
                "Different staking pools offer varying rewards, fees, and lock-up periods. "
                "Comparing them ensures you get the best returns."
            ),
            "image": "https://kauri.io/images/slide3.png",
            "queue": 1,
        },
        {
            "task_id": staking_second_task_id,
            "title": "How to Compare Pools",
            "description": (
                "Platforms like BeMo, Tonstakers, and hipo.finance provide details on rewards, fees, and risks. "
                "Choose the pool that best fits your goals."
            ),
            "image": "https://kauri.io/images/slide4.png",
            "queue": 2,
        },
    ]
    for slide in slides_second_task:
        await repo.add_one(Slide, slide)

    # Task 3: Unstake TON
    staking_third_task_data = {
        "branch_id": staking_branch_id,
        "title": "Unstake TON on Tonstakers",
        "xp": 300,
        "queue": 3,
        "task_type": TaskTypeEnum.tonstakers_unstake,
        "action_url": "https://hipo.finance/",
        "call_to_action": "You’ve learned how to unstake TON and reclaim your assets. Excellent work!",
    }
    staking_third_task_id = await repo.add_one(Task, staking_third_task_data)

    slides_third_task = [
        {
            "task_id": staking_third_task_id,
            "title": "What is Unstaking?",
            "description": (
                "Unstaking allows you to withdraw your tokens from a staking pool. "
                "After unstaking, you can use your tokens for trading or other purposes."
            ),
            "image": "https://kauri.io/images/slide5.png",
            "queue": 1,
        },
        {
            "task_id": staking_third_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Unstaking is like withdrawing money from a fixed deposit. "
                "Once withdrawn, you can use your funds as needed."
            ),
            "image": "https://kauri.io/images/slide6.png",
            "queue": 2,
        },
    ]
    for slide in slides_third_task:
        await repo.add_one(Slide, slide)

    test_user_data = {
        "telegram_id": 12345678,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "image": "https://kauri.io/images/user.png",
    }
    await repo.add_one(User, test_user_data)

    # NFT и части
    test_nft_data = {
        "image": "https://kauri.io/images/nft.png",
        "contract_address": "0xabcdef123456789",
    }
    test_nft_id = await repo.add_one(NFT, test_nft_data)

    pieces = [
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece1.png", 'branch_id': connect_wallet_branch_id, 'queue': 1},
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece1.png", 'branch_id': dedust_branch_id, 'queue': 2},
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece2.png", 'branch_id': evaa_branch_id, 'queue': 3},
        {"nft_id": test_nft_id, "image": "https://kauri.io/images/piece2.png", 'branch_id': staking_branch_id, 'queue': 4},
    ]
    for piece in pieces:
        await repo.add_one(Piece, piece)

    print("Database population completed.")
    print(f"Connect wallet task id: {connect_wallet_task_id}")



if __name__ == "__main__":
    engine = create_async_engine(DATABASE_URL, echo=True)
    SessionFactory = async_sessionmaker(engine)
    repo = TonQuestSQLAlchemyRepo(SessionFactory)
    asyncio.run(populate_database(
        engine=engine,
        repo=repo
    ))
