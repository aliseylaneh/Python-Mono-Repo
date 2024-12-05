import random
import time

import pika


def callback(ch, method, properties: pika.BasicProperties, body):
    processing_time = random.randint(1, 6)
    print(f"Message {properties.message_id}: ", body, "CPT:", processing_time)
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Messages process ended")


if __name__ == '__main__':
    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="payment_worker", on_message_callback=callback)
    channel.start_consuming()
