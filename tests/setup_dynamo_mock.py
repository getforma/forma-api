import boto3
from app.config import Config

def setup_dynamo_mock():
    """Setup the DynamoDB mock"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    # Create running sessions table
    dynamodb.create_table(
        TableName=Config.RUNNING_SESSIONS_TABLE,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
        
        # Create running sessions data table
    dynamodb.create_table(
        TableName=Config.RUNNING_SESSIONS_DATA_TABLE,
        KeySchema=[
            {'AttributeName': 'running_session_id', 'KeyType': 'HASH'},
            {'AttributeName': 'time', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
        {'AttributeName': 'running_session_id', 'AttributeType': 'S'},
            {'AttributeName': 'time', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return dynamodb