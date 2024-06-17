import pika
import os
from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv('RABBITMQ_HOST', 'localhost')
protocol = os.getenv('RABBITMQ_PROTOCOL')
user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASS')
port = os.getenv('RABBITMQ_PORT')

credentials = pika.PlainCredentials(user, password)
parameters = pika.ConnectionParameters(hostname, port, '/', credentials)

def setup_rabbitmq(queue_name, exchange_name, routing_key):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    return channel