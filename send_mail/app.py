import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

s3 = boto3.resource('s3')
client = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['MAILTABLE'])
sqs = boto3.resource('sqs')
MAILFROM = os.environ['MAILADDRESS']


def lambda_handler(event, context):

    queue = sqs.get_queue_by_name(QueueuName=os.environ['QUUENAME'])
    for rec in event['Records']:
        email = rec['body']

        bucketname = rec['messageAttributes']['bucketname']['stringValue']
        filename = rec['messageAttributes']['filename']['stringValue']
        username = rec['messageAttributes']['username']['stringValue']
        obj = s3.Object(bucketname, filename)
        response = obj.get()
        maildata = response['Body'].read().decode('utf-8')
        data = maildata.split("\n", 3)
        subject = data[0]
        body = data[2]
        response = table.update_item(Key={'email': email}, UpdateExpression="set issend=:val", ExpressionAttributeValue={
            ':val': 1
        },
            ReturnValues='UPDATED_OLD'
        )
    if response['Attributes']['issend'] == 0:
        response = client.send_email(
            Source=MAILFROM,
            ReplyToAddresses=[MAILFROM],
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Date': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Date': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    else:
        print('Resend Skip')
