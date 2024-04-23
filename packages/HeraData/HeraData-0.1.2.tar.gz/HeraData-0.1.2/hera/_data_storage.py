from enum import Enum

from elasticsearch import Elasticsearch


class StorageType(Enum):
    ELASTICSEARCH = 1


class _DataStorage:
    pass


class _ElasticSearchDataStorage(_DataStorage):
    _es_client = None
    _storage_name = None

    def __init__(
            self, storage_name, host="localhost", port=9200, auth_user='elastic',
            auth_pass='aoeui123',
    ):
        self._es_client = Elasticsearch(
            ['http://{}:{}'.format(host, port)],
            basic_auth=(auth_user, auth_pass)
        )
        self._storage_name = storage_name

    def store(self, data: dict):
        self._es_client.index(index=self._storage_name, body=data)

    def get_last(
            self, query: dict, count: int = 1, start_by_id: int = -1
    ):
        query["sort"] = [{'_index': {"order": "desc"}}]
        if start_by_id >= 0:
            query["query"] = {"range": {"_index": {"gt": start_by_id}}}
        query["size"] = count
        return self._es_client.search(index=self._storage_name, body=query)

    def search(self, query: dict):
        return self._es_client.search(index=self._storage_name, body=query)


class AresDataStorage(_ElasticSearchDataStorage):
    def __init__(
            self, host="localhost", port=9200,
            auth_user='elastic', auth_pass='aoeui123',
    ):
        super().__init__('ares', host, port, auth_user, auth_pass)


class HermesStorage(_ElasticSearchDataStorage):
    def __init__(
            self, host="localhost", port=9200,
            auth_user='elastic', auth_pass='aoeui123',
    ):
        super().__init__('hermes', host, port, auth_user, auth_pass)


class TitanStorage(_ElasticSearchDataStorage):
    def __init__(
            self, host="localhost", port=9200,
            auth_user='elastic', auth_pass='aoeui123',
    ):
        super().__init__('titan', host, port, auth_user, auth_pass)
