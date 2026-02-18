from .post import Post 

class PostRepository:
    
    def save(self, post: dict | Post) -> str:
        pass
    
    def get(self, post_id: str) -> Post | None:
        pass
    
    def list(self) -> list[Post]:
        pass
    
