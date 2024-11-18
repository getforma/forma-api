from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def put_item(self, item):
        pass

    @abstractmethod
    def get_item(self, key):
        pass

    @abstractmethod
    def query(self, **kwargs):
        pass

    @abstractmethod
    def delete_item(self, key):
        pass 