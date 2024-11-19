from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column

from database.base import BaseSqlModel


class UserTask(BaseSqlModel):
    __tablename__ = "users_tasks"
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    completed: Mapped[bool] = mapped_column(default=False)
    claimed: Mapped[bool] = mapped_column(default=False)


class UserBranch(BaseSqlModel):
    __tablename__ = "users_branches"
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    completed: Mapped[bool] = mapped_column(default=False)


class UserPiece(BaseSqlModel):
    __tablename__ = "users_pieces"
    piece_id: Mapped[int] = mapped_column(ForeignKey("pieces.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    claimed: Mapped[bool] = mapped_column(default=False)


class UserNFT(BaseSqlModel):
    __tablename__ = "users_nfts"
    nft_id: Mapped[int] = mapped_column(ForeignKey("nfts.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    claimed: Mapped[bool] = mapped_column(default=False)

    
class Slide(BaseSqlModel):
    __tablename__ = "slides"
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="slides")
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
    branch: Mapped["Branch"] = relationship("Branch", back_populates="tasks")
    title: Mapped[str] = mapped_column()
    xp: Mapped[int] = mapped_column()
    queue: Mapped[int] = mapped_column()
    task_type: Mapped[str] = mapped_column()
    action_url: Mapped[str] = mapped_column()
    call_to_action: Mapped[str] = mapped_column()
    users = relationship("User", secondary="users_tasks", back_populates="tasks")
    slides: Mapped[list[Slide]] = relationship("Slide", back_populates="task")

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
    title: Mapped[str] = mapped_column()
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="branches")
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="branch")
    users: Mapped[list["User"]] = relationship("User", secondary="users_branches", back_populates="branches")
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

    branches: Mapped[list[Branch]] = relationship("Branch", back_populates="category")

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

    tasks: Mapped[list["Task"]] = relationship("Task", secondary="users_tasks", back_populates="users")
    branches: Mapped[list["Branch"]] = relationship("Branch", secondary="users_branches", back_populates="users")
    pieces: Mapped[list["Piece"]] = relationship("Piece", secondary="users_pieces", back_populates="users")
    nfts: Mapped[list["NFT"]] = relationship("NFT", secondary="users_nfts", back_populates="users")


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
    users: Mapped[list["User"]] = relationship("User", secondary="users_pieces", back_populates="pieces")
    branch_id: Mapped[str] = mapped_column(ForeignKey("branches.id"))
    branch: Mapped["Branch"] = relationship("Branch", back_populates="pieces")
    

class NFT(BaseSqlModel):
    __tablename__ = "nfts"
    image: Mapped[str] = mapped_column()
    contract_address: Mapped[str] = mapped_column()
    users: Mapped[list["User"]] = relationship("User", secondary="users_nfts", back_populates="nfts")
    pieces: Mapped[list[Piece]] = relationship(
        "Piece", back_populates="nft"
    )

    def to_read_model(self):
        return {
            "id": self.id,
            "image": self.image,
            "contract_address": self.contract_address,
        }