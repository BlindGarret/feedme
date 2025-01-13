from datetime import datetime
from typing import List
import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Enum,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Table,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import RecipeDataBase
from .tags import RecipeTag


class RecipeCategory(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    dessert = "dessert"
    snack = "snack"
    drink = "drink"
    other = "other"


class Recipe(RecipeDataBase):
    __tablename__ = "recipes"
    __table_args__ = (
        CheckConstraint("rating >= 0"),
        CheckConstraint("rating <= 5"),
        CheckConstraint("price_rating >= 0"),
        CheckConstraint("price_rating <= 5"),
        CheckConstraint("difficulty_rating >= 0"),
        CheckConstraint("difficulty_rating <= 5"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(
        String(255), nullable=False, default="", server_default=""
    )
    ingredients: Mapped[str] = mapped_column(
        String(1024), nullable=False, default="", server_default=""
    )
    instructions: Mapped[str] = mapped_column(
        String(1024), nullable=False, default="", server_default=""
    )
    category: Mapped[RecipeCategory] = mapped_column(
        Enum(RecipeCategory),
        nullable=False,
        default=RecipeCategory.other,
        server_default="other",
    )
    tags: Mapped[List[RecipeTag]] = relationship(
        "RecipeTag", secondary="recipe_tag_links"
    )
    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        server_default="0",
    )
    price_rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        server_default="0",
    )
    difficulty_rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        server_default="0",
    )
    prep_time_mins: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    cook_time_mins: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    image_url: Mapped[str] = mapped_column(
        String(255), nullable=True, default=None, server_default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    def __repr__(self):
        return (
            "<Recipe(name='%s', description='%s', ingredients='%s', instructions='%s', category='%s', rating='%s', price_rating='%s', difficulty_rating='%s', prep_time_mins='%s', cook_time_mins='%s', image_url='%s')>"
            % (
                self.name,
                self.description,
                self.ingredients,
                self.instructions,
                self.category,
                self.rating,
                self.price_rating,
                self.difficulty_rating,
                self.prep_time_mins,
                self.cook_time_mins,
                self.image_url,
            )
        )


tag_association_table = Table(
    "recipe_tag_links",
    RecipeDataBase.metadata,
    Column("recipe_id", ForeignKey("recipes.id")),
    Column("tag_id", ForeignKey("recipe_tags.id")),
)
