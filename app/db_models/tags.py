from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import RecipeDataBase


class RecipeTag(RecipeDataBase):
    __tablename__ = "recipe_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self):
        return "<RecipeTag(name='%s')>" % (self.name)
