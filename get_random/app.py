import json
import boto3
import random

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def get_random():
    try:
        dynamodb = boto3.client('dynamodb', region_name='us-west-2')
        response = dynamodb.scan(TableName='magic_inventory')
        items = response.get('Items', [])
        if items[0]:
            return {
                'card_name': items[0]['card_name']['S'],
                'set_name': items[0]['set_name']['S']
            }
        else:
            raise ValueError("No items found in the table.")

    except ClientError as e:
        # Handle AWS service related errors
        print(f"An error occurred with DynamoDB: {e}")
        return None

    except ValueError as e:
        # Handle specific ValueError if no items are found
        print(f"Error: {e}")
        return None

    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None


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
