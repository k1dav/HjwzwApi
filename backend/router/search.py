"""搜尋 api"""
from fastapi import APIRouter
from typing import List
from dataclasses import asdict
from backend.models.base import books as model_books
from backend.resources.crawler import search_title
from backend.schemas.search import Book, BooksResponseModel
from backend.models.query import get_or_create
import asyncio

router = APIRouter()


@router.get("/title", response_model=BooksResponseModel, name="search:title")
async def search_book_title(title: str) -> BooksResponseModel:
    """搜尋書名"""
    books = await search_title(title)
    await save_books(books)
    return {"books": books}


@router.get("/book/chapters", response_model=BooksResponseModel, name="list:chapters")
async def get_book_chapters(id: str) -> BooksResponseModel:
    """取得書本章節"""
    books = await search_title(title)
    return {"books": books}


async def save_books(books: List[Book]):
    """儲存書本"""
    query = "SELECT * FROM books WHERE book_id = :book_id"

    tasks = []
    for book in books:
        tasks.append(
            get_or_create(query, {"book_id": book.book_id}, model_books, asdict(book))
        )
    return await asyncio.gather(*tasks)
