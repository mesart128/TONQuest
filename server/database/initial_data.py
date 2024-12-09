import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.ton_quest.enums import TaskTypeEnum
from apps.ton_quest.models import NFT, Branch, Category, Piece, Slide, Task, User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo  # Замените на реальный путь
from database.base import Base

import base64
import os


static_root_path = os.path.join(os.path.dirname(__file__), "../static")

def get_base_64_str(filename):
    """
    Функция для получения Base64 строки из файла.

    :param filename: Путь к файлу или его название
    :return: Base64 строка, либо пустая строка в случае ошибки
    """
    # filename = os.path.join(static_root_path, filename)
    return "static/" + filename
    try:
        # Проверяем, существует ли файл
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Файл {filename} не найден.")

        # Открываем файл и читаем его содержимое в бинарном виде
        with open(filename, "rb") as file:
            file_data = file.read()

        # Преобразуем данные файла в строку Base64
        encoded_str = base64.b64encode(file_data).decode('utf-8')
        return encoded_str
    except Exception as e:
        # В случае ошибки возвращаем пустую строку
        print(f"Ошибка при чтении файла {filename}: {e}")
        return ""


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
        "image": get_base_64_str(f"category/INTRO.png"),
        "subtitle": "Your wallet is your digital key to the TON ecosystem, allowing you to store assets, manage transactions, and interact with decentralized applications.",
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
        "image": get_base_64_str(f"category/DEX.png"),
        "subtitle": "This branch provides a beginner-friendly introduction to Dedust, guiding you through interactive tasks and clear, practical explanations.",
        # TODO - можно поменять на странице Баннер пейдж(первая страница после выбора категорий)
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
        "action_url": "https://dedust.io/swap",
        "call_to_action": "You have learned how to change one token for another, keep it up!",
    }
    dedust_first_task_id = await repo.add_one(Task, dedust_first_task_data)

    slides_dedust_tasks = [
        {
            "task_id": dedust_first_task_id,
            "title": "What is Token Swapping?",
            "description": (
                "Token swapping allows you to exchange one token for another directly on the Dedust platform. "
                "It's a quick and decentralized way to exchange resources without intermediaries."
            ),
            "image": None,  # todo я бы вставил что то типо exchange.png
            "queue": 1,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Fiat Example",
            "description": (
                "Imagine going to a currency exchange office to convert USD into EUR. "
                "Token swapping works the same way but with cryptocurrencies, without needing a bank."
            ),
            "image": None,
            "queue": 2,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Connect Your Wallet",
            "description": (
                "This ensures you can access your tokens securely."
            ),
            "image": get_base_64_str(f"dedust_swap_1.png"),
            "queue": 3,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Select swap token pair",
            "description": None,
            "image": get_base_64_str(f"dedust_swap_2.png"),
            "queue": 4,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Specify how much of the token you want to swap",
            "description": (
                "Dedust will calculate the approximate value."
            ),
            "image": get_base_64_str(f"dedust_swap_3.png"),
            "queue": 5,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Review Details and Confirm",
            "description": None,
            "image": get_base_64_str(f"dedust_swap_4.png"),
            "queue": 6,
        },
        {
            "task_id": dedust_first_task_id,
            "title": "Approve in Wallet",
            "description": None,
            "image": get_base_64_str(f"dedust_swap_5.png"),
            "queue": 7,
        },
        {
            "task_id": dedust_first_task_id,
            "title": None,
            "description": None,
            "image": get_base_64_str(f"dedust_swap_6.png"),
            "queue": 8,
        },
    ]
    for slide in slides_dedust_tasks:
        await repo.add_one(Slide, slide)

    dedust_second_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Provide liquidity on Dedust",
        "xp": 200,
        "queue": 3,
        "task_type": TaskTypeEnum.dedust_liquidity,
        "action_url": "https://dedust.io/pools/",
        "call_to_action": "You have learned how to provide liquidity and earn rewards, keep it up!",
    }
    dedust_second_task_id = await repo.add_one(Task, dedust_second_task_data)
    slides_second_task = [
        {
            "task_id": dedust_second_task_id,
            "title": "What is adding a liquidity pool",
            "description": (
                "When you create a liquidity pool, you are giving someone the opportunity to exchange the cryptocurrency pair you have locked." 
                "In return for this you receive a commission from the exchange transaction in your pool." ),
            "image": None,
            "queue": 1, 
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Fiat analogy",
            "description": (
                "Imagine that a liquidity pool is a kind of “exchange office” that contains a pair of cryptocurrencies, for example TON/USDT."
                "For the exchange to take place, participants (you, for example) contributed both TON and USDT to the pool in advance, creating a balance between these assets"),
            "image": None,
            "queue": 2,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Select liquidity pool",
            "description": "",
            "image": get_base_64_str(f"dedust_add_liquidity_1.png"),
            "queue": 3,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Deposit",
            "description": "",
            "image": get_base_64_str(f"dedust_add_liquidity_2.png"),
            "queue": 4,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Enter amount of tokens",
            "description": "",
            "image": get_base_64_str(f"dedust_add_liquidity_3.png"),
            "queue": 5,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Press Deposit",
            "description": "",
            "image": get_base_64_str(f"dedust_add_liquidity_4.png"),
            "queue": 6,
        },
        {
            "task_id": dedust_second_task_id,
            "title": "Confirm in wallet",
            "description": "",
            "image": get_base_64_str(f"dedust_add_liquidity_5.png"),
            "queue": 7,
        }
    ]
    for slide in slides_second_task:
        await repo.add_one(Slide, slide)

    dedust_third_task_data = {
        "branch_id": dedust_branch_id,
        "title": "Withdraw liquidity on Dedust",
        "xp": 300,
        "queue": 3,
        "task_type": TaskTypeEnum.dedust_withdraw,
        "action_url": "https://dedust.io/pools/",
        "call_to_action": "You have learned how to withdraw liquidity you added to the pool. ",
    }
    dedust_third_task_id = await repo.add_one(Task, dedust_third_task_data)

    slides_third_task = [
        {
            "task_id": dedust_third_task_id,
            "title": "What does it mean ?",
            "description": "Here you will withdraw liquidity/currency from the pool you created",
            "image": None,
            "queue": 1,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Fiat analogy",
            "description": "It's like withdrawing money from the reserve of an exchange office or bank",
            "image": None,
            "queue": 2,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Go to your positions",
            "description": "",
            "image": get_base_64_str(f"dedust_withdraw_liquidity_1.png"),
            "queue": 3,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Select pool",
            "description": "",
            "image": get_base_64_str(f"dedust_withdraw_liquidity_2.png"),
            "queue": 4,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Press Withdraw",
            "description": "",
            "image": get_base_64_str(f"dedust_withdraw_liquidity_3.png"),
            "queue": 5,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Press Withdraw",
            "description": "",
            "image": get_base_64_str(f"dedust_withdraw_liquidity_4.png"),
            "queue": 6,
        },
        {
            "task_id": dedust_third_task_id,
            "title": "Confirm action",
            "description": "",
            "image": get_base_64_str(f"dedust_withdraw_liquidity_5.png"),
            "queue": 7,
        },
    ]
    for slide in slides_third_task:
        await repo.add_one(Slide, slide)

    # EVAA
    evaa_category_data = {
        "head": "Lending & Borrowing",
        "title": "Intro to EVAA",
        "description": "You will learn how to use EVAA lending and borrowing tools in the TON ecosystem.",
        "image": get_base_64_str(f"category/CREDIT_LOANS.png"),
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
        "action_url": "https://app.evaa.finance/?pool=Main",
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
            "image": None,
            "queue": 1,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Fiat Analogy",
            "description": (
                "Supplying is like putting your money in a savings account. While your money is in the bank, "
                "it earns interest because the bank lends it to others or invests it."
            ),
            "image": None,
            "queue": 2,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Connect Wallet",
            "description": "",
            "image": get_base_64_str(f"evaa_supply_1.png"),
            "queue": 3,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Press '+'",
            "description": "",
            "image": get_base_64_str(f"evaa_supply_2.png"),
            "queue": 4,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Select asset",
            "description": "",
            "image": get_base_64_str(f"evaa_supply_3.png"),
            "queue": 5,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Enter amount, press Supply",
            "description": "",
            "image": get_base_64_str(f"evaa_supply_4.png"),
            "queue": 6,
        },
        {
            "task_id": evaa_first_task_id,
            "title": "Confirm in wallet",
            "description": "",
            "image": get_base_64_str(f"evaa_supply_5.png"),
            "queue": 7,
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
        "action_url": "https://app.evaa.finance/?pool=Main",
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
            "title": "Press Borrow",
            "description": "",
            "image": get_base_64_str(f"evaa_borrow_1.png"),
            "queue": 3,
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
        {
            "task_id": evaa_second_task_id,
            "title": "Select asset",
            "description": "",
            "image": get_base_64_str(f"evaa_borrow_2.png"),
            "queue": 4,
        },
        {
            "task_id": evaa_second_task_id,
            "title": "Enter amount, press Borrow",
            "description": "",
            "image": get_base_64_str(f"evaa_borrow_3.png"),
            "queue": 5,
        },
        {
            "task_id": evaa_second_task_id,
            "title": "Confirm in wallet",
            "description": "",
            "image": get_base_64_str(f"evaa_borrow_4.png"),
            "queue": 6,
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
        "task_type": TaskTypeEnum.evaa_supply,
        "action_url": "https://app.evaa.finance/?pool=Main",
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
        {
            "task_id": evaa_third_task_id,
            "title": "Press '+'",
            "description": "",
            "image": get_base_64_str(f"evaa_repay_1.png"),
            "queue": 3,
        },
        {
            "task_id": evaa_third_task_id,
            "title": "Select borrowed asset",
            "description": "",
            "image": get_base_64_str(f"evaa_repay_2.png"),
            "queue": 4,
        },
        {
            "task_id": evaa_third_task_id,
            "title": "Enter amount",
            "description": "",
            "image": get_base_64_str(f"evaa_repay_3.png"),
            "queue": 5,
        },
        {
            "task_id": evaa_third_task_id,
            "title": "Press Repay",
            "description": "",
            "image": get_base_64_str(f"evaa_repay_4.png"),
            "queue": 6,
        },
    ]
    for slide in slides_third_task:
        await repo.add_one(Slide, slide)

    evaa_fourth_task_data = {
        "branch_id": evaa_branch_id,
        "title": "Withdraw your supplied assets",
        "xp": 400,
        "queue": 4,
        "task_type": TaskTypeEnum.evaa_borrow,
        "action_url": "https://app.evaa.finance/?pool=Main",
        "call_to_action": "You have successfully withdrawn your supplied assets. Keep up the good work!",
    }
    evaa_fourth_task_id = await repo.add_one(Task, evaa_fourth_task_data)
    
    slides_fourth_task = [
        {
            "task_id": evaa_fourth_task_id,
            "title": "Select supplied asset",
            "description": "",
            "image": get_base_64_str(f"evaa_withdraw_1.png"),
            "queue": 1,
        },
        {
            "task_id": evaa_fourth_task_id,
            "title": "Press Withdraw",
            "description": "",
            "image": get_base_64_str(f"evaa_withdraw_2.png"),
            "queue": 2,
        },
        {
            "task_id": evaa_fourth_task_id,
            "title": "Enter amount",
            "description": "",
            "image": get_base_64_str(f"evaa_withdraw_3.png"),
            "queue": 3,
        },
        {
            "task_id": evaa_fourth_task_id,
            "title": "Confirm action",
            "description": "",
            "image": get_base_64_str(f"evaa_withdraw_4.png"),
            "queue": 4,
        },
    ]
    for slide in slides_fourth_task:
        await repo.add_one(Slide, slide)


    # TONSTAKERS
    staking_category_data = {
        "head": "Staking",
        "title": "Passive Income",
        "description": "Learn how to stake TON for passive income and maximize your returns.",
        "image": get_base_64_str(f"category/STAKING.png"),
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
        "title": "Stake TON",
        "xp": 200,
        "queue": 1,
        "task_type": TaskTypeEnum.tonstakers_stake,
        "action_url": "https://app.tonstakers.com/",
        "call_to_action": "You’ve successfully staked TON on Tonstakers. Great job starting your journey to passive income!",
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
        {
            "task_id": staking_first_task_id,
            "title": "Connect Wallet",
            "description": "",
            "image": get_base_64_str(f"tonstakers_stake_1.png"),
            "queue": 3,
        },
        {
            "task_id": staking_first_task_id,
            "title": "Select amount",
            "description": "",
            "image": get_base_64_str(f"tonstakers_stake_2.png"),
            "queue": 4,
        },
        {
            "task_id": staking_first_task_id,
            "title": "Press Stake",
            "description": "",
            "image": get_base_64_str(f"tonstakers_stake_3.png"),
            "queue": 5,
        },
        {
            "task_id": staking_first_task_id,
            "title": "Success",
            "description": "",
            "image": get_base_64_str(f"tonstakers_stake_4.png"),
            "queue": 6,
        },
    ]
    for slide in slides_first_task:
        await repo.add_one(Slide, slide)

    # Task 2: Unstake TON
    staking_third_task_data = {
        "branch_id": staking_branch_id,
        "title": "Unstake TON on Tonstakers",
        "xp": 300,
        "queue": 2,
        "task_type": TaskTypeEnum.tonstakers_unstake,
        "action_url": "https://app.tonstakers.com/unstake",
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
        {
            "task_id": staking_third_task_id,
            "title": "Select amount",
            "description": "",
            "image": get_base_64_str(f"tonstakers_unstake_1.png"),
            "queue": 3,
        },
        {
            "task_id": staking_third_task_id,
            "title": "Press Unstake",
            "description": "",
            "image": get_base_64_str(f"tonstakers_unstake_2.png"),
            "queue": 4,
        },
        {
            "task_id": staking_third_task_id,
            "title": "Confirm action",
            "description": "",
            "image": get_base_64_str(f"tonstakers_unstake_3.png"),
            "queue": 5,
        },
        {
            "task_id": staking_third_task_id,
            "title": "Success",
            "description": "",
            "image": get_base_64_str(f"tonstakers_unstake_4.png"),
            "queue": 6,
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
        "image": get_base_64_str('nft/NFT.webp'),
        "contract_address": "0xabcdef123456789",
    }
    test_nft_id = await repo.add_one(NFT, test_nft_data)

    pieces = [
        {
            "nft_id": test_nft_id,
            "image": "https://kauri.io/images/piece1.png",
            "branch_id": connect_wallet_branch_id,
            "queue": 1,
        },
        {
            "nft_id": test_nft_id,
            "image": "https://kauri.io/images/piece1.png",
            "branch_id": dedust_branch_id,
            "queue": 2,
        },
        {
            "nft_id": test_nft_id,
            "image": "https://kauri.io/images/piece2.png",
            "branch_id": evaa_branch_id,
            "queue": 3,
        },
        {
            "nft_id": test_nft_id,
            "image": "https://kauri.io/images/piece2.png",
            "branch_id": staking_branch_id,
            "queue": 4,
        },
    ]
    for piece in pieces:
        await repo.add_one(Piece, piece)

    print("Database population completed.")
    print(f"Connect wallet task id: {connect_wallet_task_id}")


if __name__ == "__main__":
    engine = create_async_engine(DATABASE_URL, echo=True)
    SessionFactory = async_sessionmaker(engine)
    repo = TonQuestSQLAlchemyRepo(SessionFactory)
    asyncio.run(populate_database(engine=engine, repo=repo))
