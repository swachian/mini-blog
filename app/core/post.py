from datetime import datetime
from typing import List


class Post:
    def __init__(
        self,
        title: str,
        content: str,
        author_name: str,
        tags: list[str] | None = None,
        id: str | None = None,
        views: int = 0,
        comments: list | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id   # Domain id 永远是 string
        self.title = title
        self.content = content
        self.author_name = author_name
        self.tags = tags or []
        self.views = views
        self.comments = comments or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    