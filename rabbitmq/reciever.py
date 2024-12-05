from adapter import RabbitMQAdapter, callback

if __name__ == "__main__":
    rabbitmq_adapter = RabbitMQAdapter()
    rabbitmq_adapter.channel().basic_consume(queue="wallet_status", on_message_callback=callback, auto_ack=True)
    rabbitmq_adapter.channel().start_consuming()
