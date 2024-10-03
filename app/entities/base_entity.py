#import boto3
from uuid import uuid4
from datetime  import datetime, timezone
#dynamodb = boto3.resource('dynamodb')

class BaseEntity:
    def __init__(self, table):
        self.id = str(uuid4())
        self.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        #self.table = dynamodb.Table(table)
        self.table = "./tmp/" + table + ".txt"
    
    def save(self):
        with open(self.table, 'a') as f:
            f.write(self.to_dict())
        # self.table.put_item(
        #     Item=self.to_dict()
        # )