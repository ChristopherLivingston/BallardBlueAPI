import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='us-west-2')


def get_random():
    print("In get_random")
    try:
        response = dynamodb.scan(TableName='magic_inventory')
        print(str(response))
        items = response.get('Items', [])
        if items[0]:
            print("successful return")
            return {
                "status": "success",
                'card_name': items[0]['card_name']['S'],
                'set_name': items[0]['set_name']['S']
            }
        else:
            print("not successful return")
            raise ValueError("No items found in the table.")

    except ClientError as e:
        print("ClientError")
        return {
            "status": "failure",
            "error": str(e)
        }

    except ValueError as e:
        print("ValueError")
        return {
            "status": "failure",
            "error": str(e)
        }

    except Exception as e:
        print("Exception")
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
