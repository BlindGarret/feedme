import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import index_router, recipes_router, shared_router

load_dotenv()

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=6)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount(
    "/content/recipe_images",
    StaticFiles(directory=os.getenv("IMG_DIR")),
    name="recipe_images",
)
app.include_router(index_router.router)
app.include_router(recipes_router.router)
app.include_router(shared_router.router)
