from typing import Annotated

from db_models import Recipe, get_engine
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from patching import patch_instance
from services.templating import get_templates
from sqlalchemy import Engine
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
async def recipe_page(
    request: Request,
    recipe_id: int,
    engine: Annotated[Engine, Depends(get_engine)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    with Session(engine) as session:
        recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        return templates.TemplateResponse(
            request=request,
            name="pages/recipes/edit-recipe.jinja",
            context={
                "recipe": recipe,
            },
        )


@router.patch("/partials/recipes/{recipe_id}/save")
async def save_recipe(
    request: Request,
    recipe_id: int,
    engine: Annotated[Engine, Depends(get_engine)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    form = await request.form()
    with Session(engine) as session:
        recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one_or_none()
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        patch_instance(recipe, form)
        session.commit()
        return templates.TemplateResponse(
            request=request,
            name="/partials/recipes/save.jinja",
            context={
                "recipe": recipe,
            },
        )


@router.get(
    "/partials/recipes/{recipe_id}/upload-image-modal", response_class=HTMLResponse
)
async def create_recipe_modal(
    request: Request,
    recipe_id: int,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    return templates.TemplateResponse(
        request=request,
        name="partials/recipes/image_upload.jinja",
        context={
            "id": recipe_id,
        },
    )
