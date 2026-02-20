from typing import Dict, List, Any, Optional
from app.controller.schemas.base import SearchFilter
import re

class QueryBuilder:
    OPERATOR_MAP = {
        "eq": "$eq",
        "ne": "$ne",
        "gt": "$gt",
        "gte": "$gte",
        "lt": "$lt",
        "lte": "$lte",
        "in": "$in",
        "nin": "$nin",
        "regex": "$regex",
        "contains": "$regex",  # 模糊查询
    }
    
    @classmethod
    def build_filter_query(cls, filters: List[SearchFilter]) -> Dict[str, Any]:
        """构建MongoDB查询过滤器"""
        query = {}
        
        for filter_item in filters:
            field = filter_item.field
            operator = filter_item.operator
            value = filter_item.value
            
            if operator == "contains":
                # 模糊查询，忽略大小写
                query[field] = {
                    cls.OPERATOR_MAP[operator]: f".*{re.escape(str(value))}.*",
                    "$options": "i"
                }
            elif operator in ["in", "nin"]:
                # IN/NIN操作
                query[field] = {cls.OPERATOR_MAP[operator]: value}
            else:
                # 其他操作
                if cls.OPERATOR_MAP.get(operator):
                    query[field] = {cls.OPERATOR_MAP[operator]: value}
                else:
                    # 默认使用eq
                    query[field] = value
                    
        return query
    
    @classmethod
    def build_sort_query(cls, sort_by: Optional[str], sort_order: int) -> List[tuple]:
        """构建排序查询"""
        if not sort_by:
            return []
        return [(sort_by, sort_order)]
    
    # @classmethod
    # def build_projection(cls, fields: Optional[List[str]]) -> Dict[str, int]:
    #     """构建字段投影"""
    #     if not fields:
    #         return {}
    #     return {field: 1 for field in fields}