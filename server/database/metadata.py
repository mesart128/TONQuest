"""
In this file you must import all models from a whole project to
be able alembic see all metadata to autogenerate migrations.
"""

from apps.ton_quest.models import * # noqa: F401
from database.base import Base

metadata = Base.metadata
__all__ = ["metadata"]
