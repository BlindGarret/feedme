from os import getenv

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
from dtos.recipes import CreateRecipeRequest
from db_models import Recipe

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=6)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
engine = create_engine(getenv("DB_CONNECTION_STRING") or "")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with Session(engine) as session:
        recipes = session.query(Recipe).order_by(desc(Recipe.created_at)).limit(6).all()
        return templates.TemplateResponse(
            request=request,
            name="pages/index.jinja",
            context={
                "id": "herp",
                "recipes": recipes,
            },
        )


@app.get("/index/create-recipe-modal", response_class=HTMLResponse)
async def create_recipe_modal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="components/index/create_recipe_modal.jinja",
        context={},
    )


@app.post("/index/create-recipe", response_class=HTMLResponse)
async def create_recipe(dto: CreateRecipeRequest, request: Request):
    with Session(engine) as session:
        recipe = Recipe(name=dto.name)
        session.add(recipe)
        session.commit()

        return templates.TemplateResponse(
            request=request,
            headers={"HX-Redirect": f"/recipes/{recipe.id}/edit"},
            name="components/shared/empty.jinja",
            context={},
        )


@app.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
async def recipe_page(request: Request, recipe_id: int):
    with Session(engine) as session:
        recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        return templates.TemplateResponse(
            request=request,
            name="pages/recipes/edit-recipe.jinja",
            context={
                "recipe": recipe,
            },
        )
