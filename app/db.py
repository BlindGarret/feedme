# messing around with sqlalchemy

from sqlalchemy import String, MetaData
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    declarative_base,
)

RecipeDataBase = declarative_base(metadata=MetaData(schema="recipe_data"))


class Recipe(RecipeDataBase):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return "<Recipe(name='%s')>" % (self.name)
