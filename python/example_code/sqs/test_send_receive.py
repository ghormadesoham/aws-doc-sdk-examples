import random
import boto3
import logging
import message_wrapper
import sys
import time
logger = logging.getLogger(__name__)

class SqsPerf:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        sqs = boto3.resource('sqs')
        self.q = sqs.get_queue_by_name(QueueName=queue_name)

    '''
    
    '''
    def test(self, num_messages, fifo):

        for i in range(1, num_messages):
            #print(i)
            if fifo:
             response = self.q.send_message(
             MessageAttributes={
                'version': {
                    'DataType': 'Number',
                    'StringValue': f'{i}'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': f'John Grisham {random.randint(1,200)}'
                }

             },
             MessageBody=(
                f'body: {i}'
              ),
                 MessageGroupId = f'{i}'
             )
            else:
              response = self.q.send_message(
                 MessageAttributes={
                     'version': {
                         'DataType': 'Number',
                         'StringValue': f'{i}'
                     },
                     'Author': {
                         'DataType': 'String',
                         'StringValue': f'John Grisham {random.randint(1, 200)}'
                     }

                 },
                 MessageBody=(
                     'f{i}'
                 )
             )



        batch_size = 10
        more_messages = True
        #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
        while more_messages:
            received_messages = message_wrapper.receive_messages(self.q, batch_size, 2)
            for message in received_messages:
                version = message.message_attributes.get('version')['StringValue']
                #print(f'{version}')
            if received_messages:
                message_wrapper.delete_messages(self.q, received_messages)
            else:
                more_messages = False
        print('Done.')


t = SqsPerf('MyQueue')
input_size = 100000
t1 = time.perf_counter()
t.test(input_size, False)
t2 = time.perf_counter()
std_time = t2 - t1
t = SqsPerf('TestQueue.fifo')
t1 = time.perf_counter()
t.test(input_size, True)
t2 = time.perf_counter()
fifo_time = t2 - t1

print(f'FIFO took {fifo_time} and standard took {std_time} for {input_size} messages')
# FIFO took 56.127307083 and standard took 50.6529535
