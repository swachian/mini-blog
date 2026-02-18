from datetime import datetime
from pydantic import Field
from .base import CamelModel, PyObjectId


class PostCreate(CamelModel):
    title: str
    content: str
    author_name: str


class PostResponse(CamelModel):
    id: PyObjectId = Field(validation_alias="_id")
    title: str
    content: str
    author_name: str
    created_at: datetime
    updated_at: datetime
