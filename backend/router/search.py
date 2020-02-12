"""搜尋 api"""
from fastapi import APIRouter
from backend.schemas.search import BookResponseModel

router = APIRouter()


@router.get("/books", response_model=BookResponseModel, name="search:books")
async def search_books(title: str) -> BookResponseModel:
    print(title)

