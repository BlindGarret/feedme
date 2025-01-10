from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from os import getenv

app = FastAPI()
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
