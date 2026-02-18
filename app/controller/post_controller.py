# @app.get("/")
# def read_root():
#     return {"message": "Mini Blog API running"}

from fastapi import APIRouter
from app.core.post_repository import PostRepository 
from app.core.post import Post
from .schemas.post_schema import PostCreate, PostResponse
from app.infra.mongo_post_repository import MongoPostRepository

router = APIRouter(prefix="/posts", tags=["posts"])
post_repository = MongoPostRepository()

@router.post("/", response_model = PostResponse)
async def create(post_create: PostCreate):
    post = Post(**post_create.model_dump())
    post_id = post_repository.save(post)
    post_doc = post_repository.get(post_id)
    return PostResponse.model_validate(post_doc)

@router.get("/", response_model=list[PostResponse])
async def get():
    results = post_repository.list()
    return [PostResponse.model_validate(post) for post in results]