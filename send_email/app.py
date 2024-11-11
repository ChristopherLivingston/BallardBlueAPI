import json
import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client('ses', region_name='us-west-2')

def lambda_handler(event, context):
    email = event.get('queryStringParameters', {}).get('email')
    message = event.get('queryStringParameters', {}).get('message')

    if not email or not message:
        # Identify which parameter is missing
        missing_param = "email" if not email else "message"

        return {
            'statusCode': 400,
            'body': f'{{"error": "Missing required parameter: {missing_param}"}}',
            'headers': {'Content-Type': 'application/json'}
        }

    SUBJECT = 'Contact from Ballard-Blue'
    BODY_TEXT = ""
    BODY_HTML = f"""
    <html>
      <head></head>
      <body>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong> {message}</p>
      </body>
    </html>
    """

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
        response = ses_client.send_email(
            Source=message['Source'],
            Destination=message['Destination'],
            Message=message['Message']
        )

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
