import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq
logging.basicConfig(level=logging.INFO)

class NewUserNotificationServicesSaga:
    def __init__(self, email_services):
        logging.basicConfig(level=logging.INFO)
        self.email_services=email_services
        self.queue_name = os.getenv('RABBIT_QUEUE_NEW_USER_NOTIFICATION')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.routing_key = os.getenv('RABBIT_ROUTING_KEY_USER_TOKEN')

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            logging.info('New User queue is ready to consume messages...') 
            channel.start_consuming()
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        logging.info(f'Received message: {request}')
        email = request['email']
        logging.info(f'Email: {email}')
        self.email_services.send_email(email, "Welcome", f"Welcome to our platform, your token is {request['token']}")
        logging.info(f'Notification sent to user: {email}')