from app.repositories.base_repository import BaseRepository

class MemoryRepository(BaseRepository):
    def __init__(self):
        self.items = {}

    def put_item(self, item):
        self.items[item['id']] = item
        return item

    def get_item(self, key):
        return self.items.get(key['id'])

    def query(self, **kwargs):
        # Simplified query for memory storage
        return list(self.items.values())

    def delete_item(self, key):
        if key['id'] in self.items:
            del self.items[key['id']] 