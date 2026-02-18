from pydantic import BaseModel
from typing import List

class Author(BaseModel):
    id: str
    name: str

class PostCreate(BaseModel):
    title: str
    content: str
    author: Author
    tags: List[str] = []
