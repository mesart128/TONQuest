import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class BaseSqlModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return str(self.__dict__)

    def asdict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_read_model(self):
        return self.asdict()
