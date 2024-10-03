from app.config import Config
from app.entities.base_entity import BaseEntity

class RunningSession(BaseEntity):
    def __init__(self, device_id: str, device_position: str, user_name: str):
        super().__init__(Config.RUNNING_SESSIONS_TABLE)
        self.device_id = device_id
        self.device_position = device_position
        self.user_name = user_name
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'device_id': self.device_id,
            'device_position': self.device_position,
            'created_at': self.created_at
        }