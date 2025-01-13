from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
)


# RecipeDataBase = declarative_base(metadata=MetaData(schema="recipe_data"))
class RecipeDataBase(DeclarativeBase):
    metadata = MetaData(schema="recipe_data")
