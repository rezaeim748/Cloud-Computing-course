import os
import json
import time
import pika
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "ads")

if not RABBITMQ_URL:
    raise ValueError("RABBITMQ_URL not found in environment variables!")

def consume(handler):
    params = pika.URLParameters(RABBITMQ_URL)
    params.heartbeat = 600
    params.blocked_connection_timeout = 300

    # ✅ Retry loop for RabbitMQ readiness
    for i in range(10):
        try:
            print(f"[Worker] Connecting to RabbitMQ (attempt {i+1}/10)...")
            conn = pika.BlockingConnection(params)
            break
        except pika.exceptions.AMQPConnectionError:
            print("[Worker] RabbitMQ not ready yet, retrying...")
            time.sleep(2)
    else:
        raise RuntimeError("Failed to connect to RabbitMQ after multiple attempts")

    ch = conn.channel()
    ch.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    ch.basic_qos(prefetch_count=1)

    def _cb(chx, method, properties, body):
        try:
            msg = json.loads(body.decode())
            handler(msg)
            chx.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"[Worker] Error processing message: {e}")
            chx.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    ch.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=_cb
    )

    print("[Worker] Waiting for messages...")
    ch.start_consuming()
