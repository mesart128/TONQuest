from sqlalchemy import insert, delete, update, select, desc, ChunkedIteratorResult
from apps.ton_quest.models import Branch, Category, User, Slide, NFT, Piece, Task

class BaseSQLAlchemyRepo:

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def add_one(self, model, data: dict) -> str:
        stmt = insert(model).values(**data).returning(model.id)
        return await self._execute_and_commit(stmt)

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
                return [row[0].asdict() for row in res.all()]

    async def _execute_and_fetch_one(self, stmt):
        async with self._session_factory() as session:
            async with session.begin():
                res = await session.execute(stmt)
                instance = res.scalar_one_or_none()
                return instance.asdict() if instance else None


class TonQuestSQLAlchemyRepo(BaseSQLAlchemyRepo):
    pass
