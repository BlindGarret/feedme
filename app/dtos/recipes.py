from pydantic import BaseModel


class CreateRecipeRequest(BaseModel):
    name: str
