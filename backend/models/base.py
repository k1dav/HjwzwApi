from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, text

from .common import DatetimeMixin, UUIDPrimaryKeyMixin

metadata = MetaData()

# 書本
"""Return :class: book's info.
    :param book_id: 書本 ID
    :param title: 書名
    :param author: 作者
    :param preface: 前言
"""
books = Table(
    "books",
    metadata,
    *(
        UUIDPrimaryKeyMixin
        + [
            Column("book_id", String(16), unique=True, nullable=False),
            Column("title", String(32), nullable=False),
            Column("author", String(32), nullable=False),
            Column("preface", Text),
        ]
        + DatetimeMixin
    ),
)

# chapters = Table(
#     "chapters",
#     metadata,
#     *(
#         UUIDPrimaryKeyMixin
#         + [
#             Column("chapter_id", String(16), unique=True, nullable=False),
#             Column("followers", Text),
#         ]
#         + DatetimeMixin
#     ),
# )
