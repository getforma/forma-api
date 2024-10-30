import boto3
from boto3.dynamodb.conditions import Key
from app.config import Config
class RunningSessionDataRepository:
    def __init__(self):
        self.table = boto3.resource('dynamodb', region_name='us-east-1').Table(Config.RUNNING_SESSIONS_DATA_TABLE)

    def query_data_by_session_id(self, session_id):
        response = self.table.query(
            KeyConditionExpression=Key('running_session_id').eq(session_id)
        )
        
        # Collect all items from the response
        items = response.get('Items', [])

        # Handle pagination if there are more items to retrieve
        while 'LastEvaluatedKey' in response:
            response = self.table.query(
                KeyConditionExpression=Key('running_session_id').eq(session_id),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
        
        return items
    
    def query_data_by_session_id_and_time_range(self, session_id, start_time, end_time):
        response = self.table.query(
            KeyConditionExpression=Key('running_session_id').eq(session_id) & Key('time').between(start_time, end_time)
        )
        # Collect all items from the response
        items = response.get('Items', [])

        # Handle pagination if there are more items to retrieve
        while 'LastEvaluatedKey' in response:
            response = self.table.query(
                KeyConditionExpression=Key('running_session_id').eq(session_id),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
        
        return items
    
