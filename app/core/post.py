from datetime import datetime
from typing import List


class Post:
    def __init__(
        self,
        title: str,
        content: str,
        author_name: str,
        tags: List[str] | None = None,
    ):
        self.title = title
        self.content = content
        self.author = {
            "name": author_name
        }
        self.tags = tags or []
        self.views = 0
        self.comments = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

