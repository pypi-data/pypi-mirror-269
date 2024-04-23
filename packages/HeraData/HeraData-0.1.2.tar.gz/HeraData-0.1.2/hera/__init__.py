from hera._data_storage import StorageType, _ElasticSearchDataStorage


def build_store(storage_type, **kwargs):
    if storage_type == StorageType.ELASTICSEARCH:
        return _ElasticSearchDataStorage(**kwargs)
    else:
        raise NotImplementedError(f"Storage type {storage_type} is not implemented.")

