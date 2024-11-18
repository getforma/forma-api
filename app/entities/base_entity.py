from uuid import uuid4
from datetime import datetime, timezone
from app.repositories.repository_factory import RepositoryFactory

class BaseEntity:
    def __init__(self, table):
        self.id = str(uuid4())
        self.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.repository = RepositoryFactory.get_repository(table)
    
    def save(self):
        self.repository.put_item(self.to_dict())