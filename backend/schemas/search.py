"""搜尋的 schema"""
from pydantic.dataclasses import dataclass


@dataclass
class BookResponseModel:
    book_id: str
    title: str
    author: str
    preface: str