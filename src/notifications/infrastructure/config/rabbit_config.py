import pika
import os
from dotenv import load_dotenv
import ssl

# Configuración de la conexión con SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # Puedes establecer esto en True si deseas verificar el nombre del host
ssl_context.verify_mode = ssl.CERT_NONE  # Puedes cambiar esto a ssl.CERT_REQUIRED si deseas verificar el certificado
ssl_options=pika.SSLOptions(ssl_context)

load_dotenv()
hostname = os.getenv('RABBITMQ_HOST')
protocol = os.getenv('RABBITMQ_PROTOCOL')
user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASS')
port = os.getenv('RABBITMQ_PORT')

def setup_rabbitmq(queue_name, exchange_name, routing_key):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(hostname, port, '/', credentials, ssl_options)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    return channel