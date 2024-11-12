import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    try:
        return {
            'statusCode': 200,
            'headers': {
                         "Access-Control-Allow-Origin": "*",
                         "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                         "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key",
            },
            'body': json.dumps({
                'message': 'Here is a random card!'
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
