# @app.get("/")
# def read_root():
#     return {"message": "Mini Blog API running"}

from fastapi import APIRouter, HTTPException, status, Response, Query, Depends
from app.core.post_repository import PostRepository 
from app.core.post import Post
from .schemas.post_schema import PostDto, PostResponse
from .schemas.base import SearchRequest, SearchResponse, SearchFilter
from app.infra.mongo_post_repository import MongoPostRepository
import json

router = APIRouter(prefix="/posts", tags=["posts"])
post_repository = MongoPostRepository()

@router.post("/", response_model = PostResponse)
async def create_post(post_create: PostDto):
    post = Post(**post_create.model_dump())
    post_id = await post_repository.save(post)
    post = await post_repository.get(post_id)
    return PostResponse.model_validate(post)


def parse_search_request(
    filters: str | None = Query(None),
    page: int = Query(1),
    page_size: int = Query(20, alias="pageSize"),
    sort_by: str | None = Query(None, alias="sortBy"),
    sort_order: int = Query(1, alias="sortOrder"),
    projection: str | None = Query(None),
) -> SearchRequest:

    filter_objs = []

    if filters:
        data = json.loads(filters)
        filter_objs = [SearchFilter(**f) for f in data]

    proj = None
    if projection:
        proj = json.loads(projection)

    return SearchRequest(
        filters=filter_objs,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        projection=proj,
    )
    
@router.get("/", response_model=list[PostResponse])
async def list_posts(
    searchReq: SearchRequest = Depends(parse_search_request)
    
):
    results = await post_repository.list(searchReq)
    return [PostResponse.model_validate(post) for post in results]

@router.get("/{id}", response_model = PostResponse)
async def show_students(id: str):
    if (
        post := await post_repository.get(id)
    ) is not None:
        return PostResponse.model_validate(post)
    
    return HTTPException(status_code=404, detail=f"Student {id} not found")

@router.delete("/{id}")
async def delete_post(id: str):
    deleted_count = await post_repository.delete(id)
    if deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Post {id} not found")
   
@router.put("/{id}", response_model = PostResponse) 
async def update_post(id: str, post_update: PostDto):
    if (
        post := await post_repository.get(id)        
    ) is not None:
        updates = post_update.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(post, field, value)
        await post_repository.save(post)
        return PostResponse.model_validate(post)
    
    return HTTPException(status_code=404, detail=f"Student {id} not found")
    