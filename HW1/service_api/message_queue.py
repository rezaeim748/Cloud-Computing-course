import os, pika, json

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "ads")

def publish_ad(ad_id: int):
    params = pika.URLParameters(RABBITMQ_URL)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    ch.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=json.dumps({"ad_id": ad_id}).encode(), properties=pika.BasicProperties(delivery_mode=2))
    conn.close()
