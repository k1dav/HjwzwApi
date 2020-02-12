"""搜尋的 schema"""
from pydantic.dataclasses import dataclass
from typing import List


@dataclass
class Book:
    """Book"""

    book_id: str
    title: str
    author: str
    preface: str


@dataclass
class BooksResponseModel:
    """Books"""

    books: List[Book]
