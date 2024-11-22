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
        return list(self.items.values())

    def delete_item(self, key):
        if key['id'] in self.items:
            del self.items[key['id']]

    def query_by_session_id(self, session_id):
        return [item for item in self.items.values() 
                if item.get('running_session_id') == session_id]

    def query_by_session_id_and_time_range(self, session_id, start_time, end_time):
        return [item for item in self.items.values()
                if item.get('running_session_id') == session_id
                and start_time <= item.get('time', '') <= end_time]
  