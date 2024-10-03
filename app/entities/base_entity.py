import boto3
from uuid import uuid4
from datetime  import datetime, timezone
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

class BaseEntity:
    def __init__(self, table):
        self.id = str(uuid4())
        self.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.table = dynamodb.Table(table)
    
    def save(self):
        self.table.put_item(
            Item=self.to_dict()
        )