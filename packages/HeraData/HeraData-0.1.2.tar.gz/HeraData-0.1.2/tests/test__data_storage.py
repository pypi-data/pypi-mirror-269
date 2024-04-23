import unittest
from unittest.mock import patch, MagicMock

from elasticsearch import Elasticsearch

from hera import build_store, StorageType


class TestElasticSearchDataStorage(unittest.TestCase):

    @patch.object(Elasticsearch, '__init__', return_value=None)
    def setUp(self, mock_init):
        self.es = build_store(StorageType.ELASTICSEARCH)
        self.es._es_client = MagicMock()

    def test_store(self):
        data = {'test': 'data'}
        self.es.store('index')
        self.es._es_client.index.assert_called_with(index='index', body=data)

    def test_get_last(self):
        query = {'match_all': {}}
        self.es.get_last('index', query, 10, 5)
        expected_query = {
            'match_all': {}, 'sort': [{'_index': {"order": "desc"}}], 'size': 10,
            'query': {"range": {"_index": {"gt": 5}}}
        }
        self.es._es_client.search.assert_called_with(index='index', body=expected_query)

    def test_search(self):
        query = {'match_all': {}}
        self.es.search('index', query)
        self.es._es_client.search.assert_called_with(index='index', body=query)


if __name__ == '__main__':
    unittest.main()
