import pika
import os
from dotenv import load_dotenv

load_dotenv()

def publish_message(queue_name, message):
    url = os.getenv("RABBITMQ_URI", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()
