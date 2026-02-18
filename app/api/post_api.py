# @app.get("/")
# def read_root():
#     return {"message": "Mini Blog API running"}

from fastapi import APIRouter
from app.core.post import PostCreate 

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
def create(post: PostCreate):
    
    return {"id": "aaa"}

@router.get("/")
def get():
    return 5