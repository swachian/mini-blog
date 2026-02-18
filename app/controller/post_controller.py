# @app.get("/")
# def read_root():
#     return {"message": "Mini Blog API running"}

from fastapi import APIRouter
from app.core.post_repository import PostRepository 
from .schemas.post_schema import PostCreate, PostResponse
from app.infra.mongo_post_repository import MongoPostRepository

router = APIRouter(prefix="/posts", tags=["posts"])
post_repository = MongoPostRepository()

@router.post("/", response_model = PostResponse)
async def create(post: PostCreate):
    post_data = post.model_dump(by_alias = False)
    post_id = post_repository.save(post_data)
    post_doc = post_repository.get(post_id)
    return PostResponse.model_validate(post_doc)

@router.get("/", response_model=list[PostResponse])
async def get():
    results = post_repository.list()
    return [PostResponse.model_validate(post) for post in results]