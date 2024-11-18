from app.config import Config
from app.repositories.memory_repository import MemoryRepository
from app.repositories.dynamo_repository import DynamoRepository

class RepositoryFactory:
    _instances = {}

    @classmethod
    def get_repository(cls, table_name):
        if table_name not in cls._instances:
            if Config.is_test():
                cls._instances[table_name] = MemoryRepository()
            else:
                cls._instances[table_name] = DynamoRepository(table_name)
        return cls._instances[table_name] 