from os import getenv

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=6)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
engine = create_engine(getenv("DB_CONNECTION_STRING") or "")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.jinja",
        context={
            "id": "herp",
            "recipes": ["recipe1", "recipe2", "recipe3", "recipe4", "recipe5"],
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
async def create_recipe(request: Request):
    temp_id = 42
    return templates.TemplateResponse(
        request=request,
        headers={"HX-Redirect": f"/recipes/{temp_id}"},
        name="components/shared/empty.jinja",
        context={},
    )


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def recipe_page(request: Request, recipe_id: int):
    return templates.TemplateResponse(
        request=request,
        name="pages/recipes/recipe.jinja",
        context={
            "recipe": {
                "id": recipe_id,
                "name": "temp name",
            }
        },
    )
