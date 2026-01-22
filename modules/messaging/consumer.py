import json
import os
import pika
from modules.helper.message import send_fallback
from dotenv import load_dotenv
load_dotenv()

# =====================
# RABBITMQ CONFIG
# =====================
RABBITMQ_HOST = os.getenv("RABBIT_MQ_HOST")
RABBITMQ_PORT = 5675
RABBITMQ_USER = "babe_user"
RABBITMQ_PASS = "babe_password"

EXCHANGE = "babe.exchange"
QUEUE = "babe.reply.queue"
ROUTING_KEY = "babe.command"

# =====================
# CONNECTION
# =====================
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
params = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=credentials,
    virtual_host="/",
    heartbeat=60,
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

# =====================
# DECLARE (idempotent)
# =====================
channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="direct",
    durable=True
)

channel.queue_declare(queue=QUEUE, durable=True)
channel.queue_bind(
    exchange=EXCHANGE,
    queue=QUEUE,
    routing_key=ROUTING_KEY
)

# =====================
# CALLBACK
# =====================
def callback(ch, method, properties, body):
    try:
        payload = json.loads(body.decode("utf-8"))

        print("\n📩 MESSAGE FROM RABBITMQ")
        print(json.dumps(payload, indent=2))

        success, resp = send_fallback(
            user_id=payload["baus_user_id"],
            message=payload["message"]
        )

        if not success : 
            print("❌ Failed to send fallback message")

        ch.basic_ack(method.delivery_tag)

    except Exception as e:
        print("❌ CONSUMER ERROR:", e)
        ch.basic_nack(method.delivery_tag, requeue=False)

# =====================
# RUN
# =====================
if __name__ == "__main__":
    print("🚀 api_prompting consumer listening on babe.queue")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE,
        on_message_callback=callback,
        auto_ack=False
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("🛑 Consumer stopped")
    finally:
        connection.close()
