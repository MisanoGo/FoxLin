from .base import FoxError

class StorageError(FoxError):
    pass

class DataBaseExistsError(StorageError):
    pass

class InvalidDatabaseSchema(StorageError):
    pass
