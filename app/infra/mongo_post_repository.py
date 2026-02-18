from .mongodb_provider import MongoClientProvider
from app.core.post_repository import PostRepository
from app.core.post import Post
from datetime import datetime
from bson import ObjectId

class MongoPostRepository(PostRepository):
    def __init__(self):
        super().__init__()
        self.posts = MongoClientProvider.get_db()["posts"]
        
    
    def save(self, data: dict) -> str:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        result = self.posts.insert_one(data)
        return str(result.inserted_id)
    
    def get(self, post_id: str):
        return self.posts.find_one({"_id": ObjectId(post_id)})
    
    def list(self) -> list[Post]:
        return self.posts.find()