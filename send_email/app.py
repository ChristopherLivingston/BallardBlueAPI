import json
import boto3
import os
from botocore.exceptions import ClientError

ses_client = boto3.client('ses', region_name='us-west-2')

#SENDER = os.environ['SENDER_EMAIL']  # Sender email address (must be verified in SES)
#RECIPIENT = os.environ['RECIPIENT_EMAIL']  # Recipient email address (can be unverified if in production mode)
SUBJECT = 'Test Email from AWS Lambda'
BODY_TEXT = 'This is a test email sent from AWS Lambda using Amazon SES.'
BODY_HTML = """
<html>
  <head></head>
  <body>
    <h1>This is a test email sent from AWS Lambda using Amazon SES.</h1>
  </body>
</html>
"""

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # Construct the email message
    message = {
        'Source': 'ballardbluellc@gmail.com',
        'Destination': {
            'ToAddresses': ['ballardbluellc@gmail.com'],
        },
        'Message': {
            'Subject': {
                'Data': SUBJECT
            },
            'Body': {
                'Text': {
                    'Data': BODY_TEXT
                },
                'Html': {
                    'Data': BODY_HTML
                }
            }
        }
    }

    try:
        # Send the email using SES
        response = ses_client.send_email(
            Source=message['Source'],
            Destination=message['Destination'],
            Message=message['Message']
        )

        # Log the response from SES (optional for debugging)
        print(f"Email sent! Message ID: {response['MessageId']}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Email sent successfully!',
                'message_id': response['MessageId']
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
