from typing import List

from sqlalchemy import insert, delete, update, select, desc, ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.ton_quest.models import Branch, Category, User, Slide, NFT, Piece, Task
from database.repository import NotFound


class BaseSQLAlchemyRepo:

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def add_one(self, model, data: dict) -> str:
        stmt = insert(model).values(**data).returning(model.id)
        result = await self._execute_and_commit(stmt)
        return str(result.scalar_one_or_none())

    async def delete_one(self, model, id_: str):
        stmt = delete(model).where(model.id == id_)
        await self._execute_and_commit(stmt)

    async def edit_one(self, model, id: str, data: dict) -> int:
        stmt = update(model).values(**data).filter_by(id=id).returning(model.id)
        res = await self._execute_and_commit(stmt)
        return res.scalar_one()

    async def find_all(self, model):
        stmt = select(model)
        return await self._execute_and_fetch_all(stmt)

    async def find_one(self, model, id_: str):
        stmt = select(model).where(model.id == id_)
        result = await self._execute_and_fetch_one(stmt)
        return result.scalar_one_or_none()

    async def find_one_by(self, model, **kwargs):
        stmt = select(model).filter_by(**kwargs)
        return await self._execute_and_fetch_one(stmt)

    async def find_all_by(self, model, **kwargs):
        stmt = select(model).filter_by(**kwargs).order_by(desc(model.created_at))
        return await self._execute_and_fetch_all(stmt)

    async def _execute_and_commit(self, stmt) -> ChunkedIteratorResult:
        async with self._session_factory() as session:
            async with session.begin():
                res = await session.execute(stmt)
                await session.commit()
            return res

    async def _execute_and_fetch_all(self, stmt):
        async with self._session_factory() as session:
            async with session.begin():
                res = await session.execute(stmt)
                return [row[0] for row in res.all()]

    async def _execute_and_fetch_one(self, stmt):
        async with self._session_factory() as session:
            session: AsyncSession
            async with session.begin():
                res = await session.execute(stmt)
                instance = res.scalar_one_or_none()
                return instance.asdict() if instance else None


class TonQuestSQLAlchemyRepo(BaseSQLAlchemyRepo):

    async def get_user(self, telegram_id: int) -> User:
        """Получить пользователя по ID."""
        user = await self.find_one_by(User, telegram_id=telegram_id)
        if user is None:
            raise NotFound("User not found")
        return user

    async def create_user(self, user: User) -> User:
        """Создать нового пользователя."""
        await self.add_one(User, user.asdict())  # Передача данных как словаря
        return user

    async def get_all_categories(self) -> List[Category]:
        """Получить список всех категорий."""
        stmt = select(Category).options(selectinload(Category.branches).selectinload(
            Branch.tasks).selectinload(Task.slides)
        )
        categories = await self._execute_and_fetch_all(stmt)
        return categories

    async def get_category(self, category_id: str) -> Category:
        """Получить категорию по ID."""
        category = await self.find_one(Category, category_id)
        if category is None:
            raise NotFound("Category not found")
        return category

    async def get_branch(self, branch_id: str) -> Branch:
        """Получить ветку по ID."""
        branch = await self.find_one(Branch, branch_id)
        if branch is None:
            raise NotFound("Branch not found")
        return branch

    async def get_task(self, task_id: str) -> Task:
        """Получить задачу по ID."""
        task = await self.find_one(Task, task_id)
        if task is None:
            raise NotFound("Task not found")
        return task
    
    async def get_all_nfts(self) -> List[NFT]:
        nfts = await self.find_all(NFT)
        return nfts
    
    
    
    async def add_user_wallet_address(self, user_id: int, wallet_address: str) -> User:
        user = await self.get_user(user_id)
        if user.wallet_address:
            raise ValueError("User already has address")
        user.wallet_address = wallet_address
        await self.edit_one(User, user_id, user.asdict())
        return user
    

