import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db_models import Recipe, get_engine
from app.patching import patch_instance
from app.services.templating import get_templates

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


@router.post("/partials/recipes/{recipe_id}/replace_image")
async def replace_image(
    request: Request,
    recipe_id: int,
    file: UploadFile,
    engine: Annotated[Engine, Depends(get_engine)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
    img_dir = os.getenv("IMG_DIR")
    image_name = (
        f"{uuid.uuid4().hex}.{os.path.splitext(file.filename or 'none.jpg')[1]}"
    )
    with Session(engine) as session:
        recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one_or_none()
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        with open(f"{img_dir}/{image_name}", "wb") as f:
            f.write(await file.read())

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
