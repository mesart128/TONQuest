import logging
from typing import List

from sqlalchemy import ChunkedIteratorResult, delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.ton_quest.models import (
    NFT,
    Branch,
    Category,
    Piece,
    Task,
    User,
    UserBranch,
    UserPiece,
    UserTask,
)
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
        return await self._execute_and_fetch_one(stmt)

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
                return instance if instance else None


class TonQuestSQLAlchemyRepo(BaseSQLAlchemyRepo):
    async def get_task_by_task_type(self, task_type: str) -> Task | None:
        stmt = select(Task).where(Task.task_type == task_type)
        task = await self._execute_and_fetch_one(stmt)
        return task

    async def get_nft(self, nft_id: str) -> NFT:
        smtp = select(NFT).where(NFT.id == nft_id).options(selectinload(NFT.pieces))
        nft = await self._execute_and_fetch_one(smtp)
        return nft

    async def get_nfts(self) -> List[NFT]:
        stmt = select(NFT).options(selectinload(NFT.pieces))
        nfts = await self._execute_and_fetch_all(stmt)
        return nfts

    async def get_user(self, telegram_id: int) -> User:
        """Получить пользователя по ID."""
        user = await self.find_one_by(User, telegram_id=telegram_id)
        if user is None:
            raise NotFound("User not found")
        return user

    async def get_user_by(self, **kwargs) -> User | None:
        """Получить пользователя по ID."""
        user = await self.find_one_by(User, **kwargs)
        return user

    async def create_user(self, user: User) -> User:
        """Создать нового пользователя."""
        dict_to_insert = user.asdict()
        dict_to_insert.pop("id")
        dict_to_insert.pop("created_at")
        dict_to_insert.pop("updated_at")
        await self.add_one(User, dict_to_insert)  # Передача данных как словаря
        return user

    async def add_user_wallet_address(self, user_id: int, wallet_address: str) -> User:
        user = await self.get_user(user_id)
        user.wallet_address = wallet_address
        await self.edit_one(User, user_id, user.asdict())
        return user

    async def get_all_categories(self) -> List[Category]:
        """Получить список всех категорий."""
        stmt = select(Category).options(
            selectinload(Category.branches).selectinload(Branch.tasks).selectinload(Task.slides)
        )
        categories = await self._execute_and_fetch_all(stmt)
        return categories

    async def get_category(self, category_id: str) -> Category:
        """Получить категорию по ID."""
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.branches).selectinload(Branch.tasks))
        )
        category = await self._execute_and_fetch_one(stmt)
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

    async def get_branch_with_tasks(self, branch_id: str) -> Branch:
        """Получить ветку по ID."""
        smtp = select(Branch).where(Branch.id == branch_id).options(selectinload(Branch.tasks))
        branch = await self._execute_and_fetch_one(smtp)
        return branch

    async def get_task_by(self, **kwargs) -> Task | None:
        task = await self.find_one_by(Task, **kwargs)
        return task

    async def complete_branch(self, user_id: int, branch_id: str):
        user = await self.get_user(user_id)
        user_branch = UserBranch(user_id=user_id, branch_id=branch_id, completed=True)
        await self.add_one(UserBranch, user_branch.asdict())

    async def check_branch_completed(self, user_id: int, branch_id: str) -> bool:
        user_branch = await self.find_one_by(UserBranch, user_id=user_id, branch_id=branch_id)
        if user_branch is None:
            return False
        return user_branch.completed

    async def get_user_branch(self, user_id: int, branch_id: str) -> UserBranch:
        user_branch = await self.find_one_by(UserBranch, user_id=user_id, branch_id=branch_id)
        if user_branch is None:
            raise NotFound("User branch not found")
        return user_branch

    async def create_user_branch(self, user_id: int, branch_id: str) -> UserBranch:
        user_branch = UserBranch(user_id=user_id, branch_id=branch_id, completed=False)
        await self.add_one(UserBranch, user_branch.asdict())
        return user_branch

    async def get_task(self, task_id: str) -> Task:
        """Получить задачу по ID."""
        task = await self.find_one(Task, task_id)
        if task is None:
            raise NotFound("Task not found")
        return task

    async def get_task_with_slides(self, task_id: str) -> Task:
        """Получить задачу по ID."""
        smtp = select(Task).where(Task.id == task_id).options(selectinload(Task.slides))
        task = await self._execute_and_fetch_one(smtp)
        return task

    async def get_user_task(self, user_id: str, task_id: str) -> UserTask:
        user_task = await self.find_one_by(UserTask, user_id=user_id, task_id=task_id)
        if user_task is None:
            raise NotFound("User task not found")
        return user_task

    async def check_task_completed(self, user_id: str, task_id: str) -> bool:
        user_task = await self.find_one_by(UserTask, user_id=user_id, task_id=task_id)
        if user_task is None:
            return False
        return user_task.completed

    async def claim_task(self, user_id: str, task_id: str) -> bool:
        user = await self.get_user(user_id)
        task = await self.get_task(task_id)
        user_task = await self.find_one_by(UserTask, user_id=user_id, task_id=task_id)
        if user_task is None:
            raise NotFound("User task not found")
        user_task.claimed = True
        await self.edit_one(UserTask, user_task.id, user_task.asdict())
        return True

    async def get_piece(self, piece_id: str) -> Piece:
        piece = await self.find_one(Piece, piece_id)
        if piece is None:
            raise NotFound("Piece not found")
        return piece

    async def create_user_piece(self, user_id: int, piece_id: str) -> UserPiece:
        user_piece = UserPiece(user_id=user_id, piece_id=piece_id, claimed=False)
        await self.add_one(UserPiece, user_piece.asdict())
        return user_piece

    async def get_user_piece(self, user_id: int, piece_id: str) -> UserPiece:
        user_piece = await self.find_one_by(UserPiece, user_id=user_id, piece_id=piece_id)
        if user_piece is None:
            raise NotFound("User piece not found")
        return user_piece

    async def claim_piece(self, user_id: int, piece_id: str) -> bool:
        user = await self.get_user(user_id)
        piece = await self.get_piece(piece_id)
        user_piece = await self.get_user_piece(user_id, piece_id)
        user_piece.claimed = True
        await self.edit_one(UserPiece, user_piece.id, user_piece.asdict())
        return True

    async def create_user_task(self, user_id: str, task_id: str, completed: bool = False, claimed: bool = False) -> UserTask:
        data_dict = {
            "task_id": task_id,
            "user_id": user_id,
            "completed": completed,
            "claimed": claimed,
        }
        user_task_id = await self.add_one(UserTask, data_dict)
        return await self.find_one(UserTask, user_task_id)

    async def complete_task(self, user_id: str, task_id: str) -> bool:
        user = await self.get_user_by(id=user_id)
        task = await self.get_task_by(id=task_id)
        if not all([user, task]):
            logging.error(f"User or task not found. User: {user}, Task: {task}")
            return False

        # insert UserTask with completed=True
        user_task = await self.create_user_task(user_id, task_id)
        user_task.completed = True
        return True

    async def manual_complete_task(self, user_id: str, task_id: str) -> bool:
        user = await self.get_user_by(id=user_id)
        task = await self.get_task_by(id=task_id)
        if not all([user, task]):
            logging.error(f"User or task not found. User: {user}, Task: {task}")
            return False

        user_task = await self.get_user_task(user_id, task_id)
        user_task.completed = True
        await self.edit_one(UserTask, user_task.id, user_task.asdict())
        return True
