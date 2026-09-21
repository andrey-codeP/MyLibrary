from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.depends import SessionDep
from repository.books import BooksRepository

router = APIRouter(prefix="/pages", tags=["Frontend pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/books", response_class=HTMLResponse)
async def get_books_page(request: Request, session: SessionDep):
    books = await BooksRepository.get_all_books(session)

    return templates.TemplateResponse(
        request=request,  # Передаем request сюда
        name="index.html",
        context={"books": books},  # Убрали request из context
    )
