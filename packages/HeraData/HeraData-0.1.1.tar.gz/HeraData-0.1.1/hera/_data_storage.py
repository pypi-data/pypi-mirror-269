from enum import Enum

from elasticsearch import Elasticsearch


class StorageType(Enum):
    ELASTICSEARCH = 1


class _DataStorage:
    pass


class _ElasticSearchDataStorage(_DataStorage):
    def __init__(
            self, host="localhost", port=9200, auth_user='elastic', auth_pass='aoeui123'
    ):
        self._es_client = Elasticsearch(
            ['http://{}:{}'.format(host, port)],
            basic_auth=(auth_user, auth_pass)
        )

    def store(self, store_name: str, data: dict):
        self._es_client.index(index=store_name, body=data)

    def get_last(
            self, store_name: str, query: dict, count: int = 1, start_by_id: int = -1
    ):
        query["sort"] = [{'_index': {"order": "desc"}}]
        if start_by_id >= 0:
            query["query"] = {"range": {"_index": {"gt": start_by_id}}}
        query["size"] = count
        return self._es_client.search(index=store_name, body=query)

    def search(self, store_name: str, query: dict):
        return self._es_client.search(index=store_name, body=query)
