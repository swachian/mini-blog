
from pymongo import MongoClient

class MongoClientProvider:
    _client = None
    uri = "mongodb://admin:admin123@localhost:27017"
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client =  MongoClient(cls.uri, maxPoolSize = 50, minPoolSize = 5)
        return cls._client
            
    @classmethod
    def get_db(cls):
        return cls.get_client()["mini_blog"] 

