import boto3

import logging
#https://us-east-1.console.aws.amazon.com/sqs/v2/home?region=us-east-1#/queues/https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F252447871356%2FTestQueue.fifo
queue_name = 'MyQueue'

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queue_name)
response = queue.send_message(
    MessageAttributes ={
        'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        },
        'Author': {
            'DataType': 'String',
            'StringValue': 'John Grisham'
        },
        'WeeksOn': {
            'DataType': 'Number',
            'StringValue': '6'
        }
    },
    MessageBody=(
        'Information about current NY Times fiction bestseller for '
        'week of 12/11/2016.'
    )
        )


print(response['MessageId'])
# botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the SendMessage operation: Access to the resource https://sqs.us-east-1.amazonaws.com/ is denied
#https://aws.amazon.com/premiumsupport/knowledge-center/sqs-queue-access-permissions/
# https://aws.amazon.com/premiumsupport/knowledge-center/sqs-accessdenied-errors/.