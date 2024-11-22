from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseSqlModel


class UserTask(BaseSqlModel):
    __tablename__ = "users_tasks"
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    completed: Mapped[bool] = mapped_column(default=False)
    claimed: Mapped[bool] = mapped_column(default=False)


class UserBranch(BaseSqlModel):
    __tablename__ = "users_branches"
    branch_id: Mapped[str] = mapped_column(ForeignKey("branches.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    completed: Mapped[bool] = mapped_column(default=False)


class UserPiece(BaseSqlModel):
    __tablename__ = "users_pieces"
    piece_id: Mapped[str] = mapped_column(ForeignKey("pieces.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    claimed: Mapped[bool] = mapped_column(default=False)


class UserNFT(BaseSqlModel):
    __tablename__ = "users_nfts"
    nft_id: Mapped[str] = mapped_column(ForeignKey("nfts.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    claimed: Mapped[bool] = mapped_column(default=False)


class Slide(BaseSqlModel):
    __tablename__ = "slides"
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="slides")
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
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
    branch_id: Mapped[str] = mapped_column(ForeignKey("branches.id"), nullable=True)
    branch: Mapped["Branch"] = relationship("Branch", back_populates="tasks")
    title: Mapped[str] = mapped_column()
    xp: Mapped[int] = mapped_column()
    queue: Mapped[int] = mapped_column()
    task_type: Mapped[str] = mapped_column()
    action_url: Mapped[str] = mapped_column()
    call_to_action: Mapped[str] = mapped_column()
    users = relationship("User", secondary="users_tasks", back_populates="tasks")
    slides: Mapped[list[Slide]] = relationship("Slide", back_populates="task", lazy="noload")

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
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="branch", lazy="subquery")
    users: Mapped[list["User"]] = relationship(
        "User", secondary="users_branches", back_populates="branches"
    )
    pieces: Mapped[list["Piece"]] = relationship("Piece", back_populates="branch")

    def to_read_model(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "title": self.title,
            "tasks": [task.to_read_model() for task in self.tasks],
            "pieces": [piece.to_read_model() for piece in self.pieces]
        }


class Category(BaseSqlModel):
    __tablename__ = "categories"
    head: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column()

    branches: Mapped[list[Branch]] = relationship(
        "Branch", back_populates="category", lazy="subquery"
    )

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
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    wallet_address: Mapped[str] = mapped_column(nullable=True)

    tasks: Mapped[list["Task"]] = relationship(
        "Task", secondary="users_tasks", back_populates="users"
    )
    branches: Mapped[list["Branch"]] = relationship(
        "Branch", secondary="users_branches", back_populates="users"
    )
    pieces: Mapped[list["Piece"]] = relationship(
        "Piece", secondary="users_pieces", back_populates="users"
    )
    nfts: Mapped[list["NFT"]] = relationship("NFT", secondary="users_nfts", back_populates="users")

    completed_tasks: Mapped[list[UserTask]] = relationship(
        "UserTask", primaryjoin="and_(User.id==UserTask.user_id, UserTask.completed==True)",
        viewonly=True,
    )

    completed_branches: Mapped[list[UserBranch]] = relationship(
        "UserBranch", primaryjoin="and_(User.id==UserBranch.user_id, UserBranch.completed==True)",
        viewonly=True,
    )

    claimed_pieces: Mapped[list[UserPiece]] = relationship(
        "UserPiece", primaryjoin="and_(User.id==UserPiece.user_id, UserPiece.claimed==True)",
        viewonly=True,
    )

    def to_read_model(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "image": self.image,
            "wallet_address": self.wallet_address,
            "completed_tasks": [task.task_id for task in self.completed_tasks],
            "claimed_tasks": [task.task_id for task in self.completed_tasks if task.claimed],
            "completed_branches": [branch.branch_id for branch in self.completed_branches],
            "claimed_pieces": [piece.piece_id for piece in self.claimed_pieces],
            "nfts": [nft.to_read_model() for nft in self.nfts],
        }


class Piece(BaseSqlModel):
    __tablename__ = "pieces"
    nft_id: Mapped[str] = mapped_column(ForeignKey("nfts.id"))
    image: Mapped[str] = mapped_column()
    users: Mapped[list["User"]] = relationship(
        "User", secondary="users_pieces", back_populates="pieces"
    )
    branch_id: Mapped[str] = mapped_column(ForeignKey("branches.id"), nullable=True)
    branch: Mapped["Branch"] = relationship("Branch", back_populates="pieces")
    queue: Mapped[int] = mapped_column(default=0, nullable=True)
    nft: Mapped["NFT"] = relationship("NFT", back_populates="pieces")

    def to_read_model(self):
        return {
            "id": self.id,
            "nft_id": self.nft_id,
            "image": self.image,
            "branch_id": self.branch_id,
            "queue": self.queue,
        }


class NFT(BaseSqlModel):
    __tablename__ = "nfts"
    image: Mapped[str] = mapped_column()
    contract_address: Mapped[str] = mapped_column()
    users: Mapped[list["User"]] = relationship(
        "User", secondary="users_nfts", back_populates="nfts"
    )
    pieces: Mapped[list[Piece]] = relationship("Piece", back_populates="nft")

    def to_read_model(self):
        return {
            "id": self.id,
            "image": self.image,
            "contract_address": self.contract_address,
            "pieces": [piece.to_read_model() for piece in self.pieces],
        }
