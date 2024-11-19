from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column

from database import BaseSqlModel

users_tasks = Table(
    "users_tasks",
    BaseSqlModel.metadata,
    Column("task_id", ForeignKey("tasks.id")),
    Column("user_id", ForeignKey("users.id")),
    Column("completed", Mapped[bool]),
    Column("claimed", Mapped[bool]),
)

users_branches = Table(
    "users_branches",
    BaseSqlModel.metadata,
    Column("branch_id", ForeignKey("branches.id")),
    Column("user_id", ForeignKey("users.id")),
    Column("completed", Mapped[bool]),
)

users_pieces = Table(
    "users_pieces",
    BaseSqlModel.metadata,
    Column("piece_id", ForeignKey("pieces.id")),
    Column("user_id", ForeignKey("users.id")),
    Column("claimed", Mapped[bool]),
)

users_nfts = Table(
    "users_nfts",
    BaseSqlModel.metadata,
    Column("nft_id", ForeignKey("nfts.id")),
    Column("user_id", ForeignKey("users.id")),
    Column("claimed", Mapped[bool]),
)
    
class Slide(BaseSqlModel):
    __tablename__ = "slides"
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    queue: Mapped[int] = mapped_column()

    def to_read_model(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "queue": self.queue,
        }


class Task(BaseSqlModel):
    __tablename__ = "tasks"
    branch_id: Mapped[str] = mapped_column(ForeignKey("branches.id"))
    title: Mapped[str] = mapped_column()
    xp: Mapped[int] = mapped_column()
    queue: Mapped[int] = mapped_column()
    task_type: Mapped[str] = mapped_column()
    action_url: Mapped[str] = mapped_column()
    call_to_action: Mapped[str] = mapped_column()

    slides: Mapped[Slide] = relationship()

    def to_read_model(self):
        return {
            "id": self.id,
            "branch_id": self.branch_id,
            "title": self.title,
            "xp": self.xp,
            "queue": self.queue,
            "task_type": self.task_type,
            "action_url": self.action_url,
            "call_to_action": self.call_to_action,
            "slides": [slide.to_read_model() for slide in self.slides],
        }

class Branch(BaseSqlModel):
    __tablename__ = "branches"
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    
    tasks: Mapped[Task] = relationship()

    def to_read_model(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "tasks": [task.to_read_model() for task in self.tasks],
        }    


class Category(BaseSqlModel):
    __tablename__ = "categories"
    head: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column()

    branches: Mapped[Branch] = relationship()

    def to_read_model(self):
        return {
            "id": self.id,
            "head": self.head,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "subtitle": self.subtitle,
            "branches": [branch.to_read_model() for branch in self.branches],
        }
    
class UserTask(BaseSqlModel):
    __tablename__ = "user_tasks"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"))
    completed: Mapped[bool] = mapped_column()
    claimed: Mapped[bool] = mapped_column()

    def to_read_model(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "completed": self.completed,
            "claimed": self.claimed,
        }

class User(BaseSqlModel):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column()
    username: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    wallet_address: Mapped[str] = mapped_column()

    tasks = relationship("Task", secondary=users_tasks)
    branches = relationship("Branch", secondary=users_branches)
    pieces = relationship("Piece", secondary=users_pieces)
    nfts = relationship("NFT", secondary=users_nfts)

    def to_read_model(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "image": self.image,
            "wallet_address": self.wallet_address,
        }

class Piece(BaseSqlModel):
    __tablename__ = "pieces"
    nft_id: Mapped[str] = mapped_column(ForeignKey("nfts.id"))
    image: Mapped[str] = mapped_column()
    

class NFT(BaseSqlModel):
    __tablename__ = "nfts"
    image: Mapped[str] = mapped_column()
    contract_address: Mapped[str] = mapped_column()

    pieces: Mapped[Piece] = relationship()

    def to_read_model(self):
        return {
            "id": self.id,
            "image": self.image,
            "contract_address": self.contract_address,
        }