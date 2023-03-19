import boto3
import logging

logger = logging.getLogger(__name__)

sqs = boto3.resource('sqs')
queue_name = 'MyQueue'
queue = sqs.get_queue_by_name(QueueName=queue_name)

messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

for msg in messages:
    logger.info("Received message: %s: %s", msg.message_id, msg.body)