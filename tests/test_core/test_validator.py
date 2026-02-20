import pytest 

from app.core.post import Post

class TestPost:
    
    def test_new_post(self):
        post = Post(title="aaa", content="bbb", author_name="abc")
        assert post.title == "aaa"
        
