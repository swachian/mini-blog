import pytest 

from app.core.post import Post
from app.controller.query_builder import QueryBuilder
from app.controller.schemas.base import SearchFilter


class TestPost:
    
    def test_new_post(self):
        post = Post(title="aaa", content="bbb", author_name="abc")
        assert post.title == "aaa"
        
    def test_build_filter_query_eq(self):
        """测试等于操作符"""
        filters = [SearchFilter(field="age", operator="eq", value=25)]
        query = QueryBuilder.build_filter_query(filters)
        assert query == {"age": {"$eq": 25}}
        
    def test_build_filter_query_gt(self):
        """测试大于操作符"""
        filters = [SearchFilter(field="age", operator="gt", value=25)]
        query = QueryBuilder.build_filter_query(filters)
        assert query == {"age": {"$gt": 25}}
    
    def test_build_filter_query_gte(self):
        """测试大于等于操作符"""
        filters = [SearchFilter(field="age", operator="gte", value=25)]
        query = QueryBuilder.build_filter_query(filters)
        assert query == {"age": {"$gte": 25}}