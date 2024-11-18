import boto3
from app.repositories.base_repository import BaseRepository

class DynamoRepository(BaseRepository):
    def __init__(self, table_name, region='us-east-1'):
        self.table = boto3.resource('dynamodb', region_name=region).Table(table_name)

    def put_item(self, item):
        return self.table.put_item(Item=item)

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def query(self, **kwargs):
        response = self.table.query(**kwargs)
        return response.get('Items', [])

    def delete_item(self, key):
        return self.table.delete_item(Key=key) 