from sqlalchemy.orm import Mapped, mapped_column

from core.database.base import BaseSqlModel


class Category(BaseSqlModel):
    __tablename__ = "categories"
    head: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column()

    def to_read_model(self):
        return {
            "id": self.id,
            "head": self.head,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "subtitle": self.subtitle,
        }


