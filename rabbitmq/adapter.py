import pika


class RabbitMQAdapter:
    def __init__(self):
        self._connection = pika.BlockingConnection()
        self._channel = self._connection.channel()

    def close_connection(self):
        self._connection.close()

    def declare_exchange(self, exchange, exchange_type: str):
        self._channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    def _bind_queue(self, exchange, queue, routing_key=""):
        self._channel.queue_bind(
            exchange=exchange, routing_key=routing_key, queue=queue
        )

    def declare_queue(self, exchange, queue_name, routing_key=""):
        self._channel.queue_declare(queue=queue_name)
        self._bind_queue(
            exchange=exchange, queue=queue_name, routing_key=routing_key
        )

    def channel(self):
        return self._channel


def callback(ch, method, properties: pika.BasicProperties, body):
    print("Message: ", body, properties.correlation_id)
