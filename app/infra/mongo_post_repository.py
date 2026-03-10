from .mongodb_provider import MongoClientProvider
from app.core.post_repository import PostRepository
from app.core.post import Post
from app.controller.schemas.base import SearchFilter, SearchRequest, SearchResponse
from app.controller.query_builder import QueryBuilder
from datetime import datetime
from bson import ObjectId

class MongoPostRepository(PostRepository):
    def __init__(self):
        super().__init__()
        self.posts = MongoClientProvider.get_db()["posts"]
        
    
    async def save(self, post: dict | Post) -> str:
        if not post.id:
            result = await self.posts.insert_one(self._to_dict(post))
            return str(result.inserted_id)
        else:
            await self.posts.update_one({"_id": post.id}, {"$set": self._to_dict(post)})
            return post.id
    
    async def get(self, post_id: str) -> Post:
        doc = await self.posts.find_one({"_id": ObjectId(post_id)})
        return Post(**doc)
    
    async def list(self, searchReq: SearchRequest | None) -> list[Post]:
        if not searchReq:
            searchReq = SearchRequest() 
        query = QueryBuilder.build_filter_query(searchReq.filters)
        docs = await self.posts.find(query).skip((searchReq.page - 1) * searchReq.page_size).limit(searchReq.page_size).to_list()
        return [Post(**doc) for doc in docs]
    
    async def delete(self, id: str) -> int:
        delete_result = await self.posts.delete_one({"_id": ObjectId(id)})
        return delete_result.deleted_count
    
    
    def _from_dict(self, doc: dict) -> Post:
        return Post(
            id = str(doc["_id"]),
            title = doc["title"],
            content = doc["content"],
            author_name = doc["author_name"],
            tags = doc.get("tags"),
            views = doc.get("views", 0),
            comments = doc.get("comments", []),
            created_at = doc.get("created_at"),
            updated_at = doc.get("updated_at"),
        )

    def _to_dict(self, post: Post) -> dict:
        doc = {
            "title": post.title,
            "content": post.content,
            "author_name": post.author_name,
            "tags": post.tags,
            "views": post.views,
            "comments": post.comments,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        
        if post.id and ObjectId.is_valid(post.id):
            doc["_id"] = ObjectId(post.id)
        
        return doc
        