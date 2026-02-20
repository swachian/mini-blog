from pydantic import BaseModel, ConfigDict, BeforeValidator, Field
from typing import Annotated, Any
from bson import ObjectId


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

def str_objectid(v):
    if isinstance(v, ObjectId):
        return str(v)
    return v

PyObjectId = Annotated[str, BeforeValidator(str_objectid)]

class SearchFilter(CamelModel):
    field: str
    operator: str  # eq, ne, gt, gte, lt, lte, in, nin, regex, contains
    value: Any
    
class SearchRequest(CamelModel):
    filters: list[SearchFilter] = Field(default_factory=list)
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str | None = None
    sort_order: int = Field(1, ge=-1, le=1)  # 1 for ascending, -1 for descending
    projection: list[str] | None = None  # 指定返回的字段

class SearchResponse(CamelModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[dict[str, Any]]