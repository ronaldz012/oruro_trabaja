from django.core.files.storage import storages


def private_storage():
    """Storage privado actual: local o S3/R2 según STORAGES."""
    return storages["private"]
