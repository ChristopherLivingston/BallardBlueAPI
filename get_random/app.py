import json
import boto3
import random
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='us-west-2')


def get_random():
    try:
        random_uuid = str(uuid.uuid4())
        response = dynamodb.scan(
            TableName='magic_inventory',
            FilterExpression='row_id > :random_uuid',
            ExpressionAttributeValues={
                ':random_uuid': {'S': random_uuid}
            },
            Limit=100
        )
        if 'Items' in response:
            item_count = response['Count']
            random_index = 0
            if item_count > 0:
                random_index = random.randint(0, item_count-1)
            items = response.get('Items', [])
            return {
                "status": "success",
                'card_name': items[random_index]['card_name']['S'],
                'set_name': items[random_index]['set_name']['S']
            }
        else:
            raise ValueError("No items found in the table.")

    except ClientError as e:
        print("ClientError: " + str(e))
        return {
            "status": "failure",
            "error": str(e)
        }

    except ValueError as e:
        print("ValueError: " + str(e))
        return {
            "status": "failure",
            "error": str(e)
        }

    except Exception as e:
        print("Exception: " + str(e))
        return {
            "status": "failure",
            "error": str(e)
        }


def lambda_handler(event, context):
    try:
        random_card = get_random()
        return {
            'statusCode': 200,
            'headers': {
                         "Access-Control-Allow-Origin": "*",
                         "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                         "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key",
            },
            'body': json.dumps({
                'message': random_card
            })
        }
    except ClientError as e:
        # Handle errors that occur during sending email
        error_message = e.response['Error']['Message']
        print(f"Error sending email: {error_message}")

        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to send email',
                'error': error_message
            })
        }
