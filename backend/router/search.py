"""搜尋 api"""
from fastapi import APIRouter

from backend.resources.crawler import search_title
from backend.schemas.search import BooksResponseModel

router = APIRouter()


@router.get("/books", response_model=BooksResponseModel, name="search:books")
async def search_books(title: str) -> BooksResponseModel:
    """搜尋書名"""
    books = await search_title(title)
    return {"books": books}
