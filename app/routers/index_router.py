from typing import Annotated

from db_models import Recipe, get_engine
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.templating import get_templates
from sqlalchemy import Engine, desc
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    engine: Annotated[Engine, Depends(get_engine)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
):
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
