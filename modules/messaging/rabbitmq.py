import pika
import json
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

EXCHANGE = "babe.exchange"
QUEUE = "babe.queue"
ROUTING_KEY = "babe.command"

def publish_babe_message(payload: dict):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # declare (idempotent)
    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="direct",
        durable=True
    )

    channel.queue_declare(
        queue=QUEUE,
        durable=True
    )

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=QUEUE,
        routing_key=ROUTING_KEY
    )

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()
