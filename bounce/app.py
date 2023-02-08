import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['MAILTABLE'])


def lambda_handler(event, context):

    queue = sqs.get_queue_by_name(QueueuName=os.environ['QUUENAME'])
    for rec in event['Records']:
        message = rec['Sns']['Message']

        data = json.loads(message)
        if data['notificationType'] == 'Bounce':
            bounces = data['bounce']['bounceRecipients']
            for b in bounces:
                email = b['emailAddress']
                response = table.update_item(
                    Key={
                        'email': email
                    },
                    UpdateExpression="set issend=:val",
                    ExpressionAttributeValue={
                        ':val': 1
                    }
                )
