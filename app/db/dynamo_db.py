import boto3
from botocore.exceptions import ClientError
from app.config import config

class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=config.AWS_REGION, endpoint_url=config.DYNAMODB_ENDPOINT)

    def get_item(self, table_name, key):
        table = self.dynamodb.Table(table_name)
        try:
            response = table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item from {table_name}: {e.response['Error']['Message']}")
            return None

    def put_item(self, table_name, item):
        table = self.dynamodb.Table(table_name)
        try:
            table.put_item(Item=item)
            return True
        except ClientError as e:
            print(f"Error putting item to {table_name}: {e.response['Error']['Message']}")
            return False

    def update_item(self, table_name, key, update_expression, expression_attribute_values):
        table = self.dynamodb.Table(table_name)
        try:
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return True
        except ClientError as e:
            print(f"Error updating item in {table_name}: {e.response['Error']['Message']}")
            return False

    def query(self, table_name, key_condition_expression, expression_attribute_values):
        table = self.dynamodb.Table(table_name)
        try:
            response = table.query(
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=False,
                Limit=1
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error querying {table_name}: {e.response['Error']['Message']}")
            return []

    def scan(self, table_name, filter_expression=None, expression_attribute_values=None):
        table = self.dynamodb.Table(table_name)
        try:
            if filter_expression and expression_attribute_values:
                response = table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_attribute_values
                )
            else:
                response = table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error scanning {table_name}: {e.response['Error']['Message']}")
            return []

db = DynamoDB()