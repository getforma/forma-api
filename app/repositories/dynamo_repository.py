import boto3
from boto3.dynamodb.conditions import Key
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
        items = response.get('Items', [])
        
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = self.table.query(
                **kwargs,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
            
        return items

    def delete_item(self, key):
        return self.table.delete_item(Key=key)

    def query_by_session_id(self, session_id):
        return self.query(
            KeyConditionExpression=Key('running_session_id').eq(session_id)
        )

    def query_by_session_id_and_time_range(self, session_id, start_time, end_time):
        return self.query(
            KeyConditionExpression=Key('running_session_id').eq(session_id) & 
                                 Key('time').between(start_time, end_time)
        ) 