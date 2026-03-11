from elasticsearch import AsyncElasticsearch

class EsProvider:
    _es = AsyncElasticsearch("http://localhost:9200")

    @classmethod
    def get_es(cls):
        return cls._es


