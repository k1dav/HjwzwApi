from datetime import datetime

from elasticsearch_dsl import (
    Boolean,
    Completion,
    Date,
    Document,
    InnerDoc,
    Keyword,
    Nested,
    Text,
    analyzer,
)


class DatatimeMixin:
    created_at = Date()
    updated_at = Date()

    def save(self, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super().save(**kwargs)


class Bookmark(InnerDoc):
    user_id = Keyword(required=True)
    created_at = Date()


class Chapter(Document, DatatimeMixin):
    book_id = Keyword(required=True)  # postgres id
    content = Text()
    bookmarks = Nested(Bookmark)

    class Index:
        name = "chapter"

    def add_bookmark(self, user_id:str):
        """增加書籤"""
        self.bookmarks.append(
          Bookmark(user_id=user_id, created_at=datetime.now())
