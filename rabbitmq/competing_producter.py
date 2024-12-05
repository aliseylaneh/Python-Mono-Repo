import random
import time

import pika


def producer():
    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.queue_declare("payment_worker")
    channel.basic_qos(prefetch_count=1)
    message = "test message for competing/consumer pattern"
    message_id = 1
    while True:
        """
        Testing out competing consumers pattern
        """
        processing_time = random.randint(1, 4)
        channel.basic_publish(exchange='', routing_key='payment_worker', body=message,
                              properties=pika.BasicProperties(message_id=str(message_id)))
        print(f"Sent {message_id}: ", message, " PPT", processing_time)
        time.sleep(processing_time)
        message_id += 1


if __name__ == '__main__':
    producer()
