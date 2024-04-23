import unittest
from hera import build_store, StorageType, _ElasticSearchDataStorage


class TestHeraData(unittest.TestCase):

    def test_elasticsearch_storage_type(self):
        # setup
        kwargs = {'host': 'localhost', 'port': 9200}

        # action
        result = build_store(StorageType.ELASTICSEARCH, **kwargs)

        # verify
        self.assertIsInstance(result, _ElasticSearchDataStorage)

    def test_unknown_storage_type(self):
        # setup
        storage_type = 'unknown_storage'

        # action & verify
        with self.assertRaises(NotImplementedError) as context:
            build_store(storage_type)

        self.assertEqual(
            str(context.exception), f"Storage type {storage_type} is not implemented."
        )


if __name__ == '__main__':
    unittest.main()
