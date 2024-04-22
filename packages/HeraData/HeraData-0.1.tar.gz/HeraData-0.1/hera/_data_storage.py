from elasticsearch import Elasticsearch


class _DataStorage:
    pass


class _ElasticSearchDataStorage(_DataStorage):
    def __init__(self, host="localhost", port=9200):
        self._host = host
        self._port = port
        self._es = Elasticsearch([{"host": host, "port": port}])

    def store(self, store_name: str, data: dict):
        self._es.index(index=store_name, body=data)

    def get_last(
            self, store_name: str, query: dict, count: int = 1, start_by_id: int = -1
    ):
        query["sort"] = [{'_index': {"order": "desc"}}]
        if start_by_id >= 0:
            query["query"] = {"range": {"_index": {"gt": start_by_id}}}
        query["size"] = count
        return self._es.search(index=store_name, body=query)

    def search(self, store_name: str, query: dict):
        return self._es.search(index=store_name, body=query)
