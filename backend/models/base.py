from uuid import uuid4
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()

# 書本
"""Return :class: book's info.
    :param book_id: 書本 ID
    :param title: 書名
    :param author: 作者
    :param preface: 前言
"""
books = sqlalchemy.Table(
    "books",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("book_id", String(16), unique=True, nullable=False),
    Column("title", String(32), nullable=False),
    Column("author", String(32), nullable=False),
    Column("preface", Text),
    
    Column("created_at", DateTime, nullable=False, default=datetime.now),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    ),
)
