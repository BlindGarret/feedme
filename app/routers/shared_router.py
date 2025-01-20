from typing import Annotated

from db_models import Recipe, get_engine
from dtos.recipes import CreateRecipeRequest
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.templating import get_templates
from sqlalchemy import Engine
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/partials/shared/create-recipe-modal", response_class=HTMLResponse)
async def create_recipe_modal(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    return templates.TemplateResponse(
        request=request,
        name="partials/shared/create_recipe_modal.jinja",
        context={},
    )


@router.post("/partials/shared/create-recipe", response_class=HTMLResponse)
async def create_recipe(
    dto: CreateRecipeRequest,
    request: Request,
    engine: Annotated[Engine, Depends(get_engine)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    with Session(engine) as session:
        recipe = Recipe(name=dto.name)
        session.add(recipe)
        session.commit()

        return templates.TemplateResponse(
            request=request,
            headers={"HX-Redirect": f"/recipes/{recipe.id}/edit"},
            name="partials/shared/empty.jinja",
            context={},
        )
