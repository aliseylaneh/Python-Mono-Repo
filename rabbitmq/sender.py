import pika

from adapter import RabbitMQAdapter


def topic_fanout_direct():
    import json
    import uuid
    rabbitmq_adapter = RabbitMQAdapter()
    exchange_name = "product_status"
    binding_key_one = "foo.bar"
    binding_key_two = "oof.bar"

    rabbitmq_adapter.declare_exchange(exchange=exchange_name, exchange_type="topic")
    rabbitmq_adapter.declare_queue(exchange=exchange_name, queue_name="Queue-1", routing_key="foo.*")
    rabbitmq_adapter.declare_queue(exchange=exchange_name, queue_name="Queue-2", routing_key="*.bar")

    test_message: str = json.dumps({"product_id": "155123", "quantity": 5})
    rabbitmq_adapter.channel().basic_publish(exchange=exchange_name, routing_key=binding_key_one, body=test_message,
                                             properties=pika.BasicProperties(correlation_id=str(uuid.uuid4())))

    rabbitmq_adapter.channel().basic_publish(exchange=exchange_name, routing_key=binding_key_two, body=test_message,
                                             properties=pika.BasicProperties(correlation_id=str(uuid.uuid4())))

    rabbitmq_adapter.close_connection()


def header():
    import uuid
    rabbitmq_adapter = RabbitMQAdapter()
    exchange_name = "wallet_log"
    rabbitmq_adapter.declare_exchange(exchange=exchange_name, exchange_type="headers")
    rabbitmq_adapter.declare_queue(exchange=exchange_name, queue_name="wallet_status")
    headers = {
        'type': 'important',
        'x-match': 'any'  # 'any' means any of the headers match
    }
    rabbitmq_adapter.channel().queue_bind(exchange=exchange_name, queue="wallet_status", arguments=headers)
    headers_to_publish = {
        'type': 'important',  # Matches the type header defined in the binding
        'priority': 'high'  # Another header that can be used for routing
    }
    message_body = f"withdraw on wallet '5512331-123341' by user {str(uuid.uuid4())} for amount of 4,850,000 Rials"
    rabbitmq_adapter.channel().basic_publish(
        exchange='wallet_log',
        routing_key='',  # Routing key is empty for header exchange
        body=message_body,
        properties=pika.BasicProperties(
            correlation_id=str(uuid.uuid4()),
            headers=headers_to_publish
        )
    )


if __name__ == "__main__":
    # topic_fanout_direct()
    header()
