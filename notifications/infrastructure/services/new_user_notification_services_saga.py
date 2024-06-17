import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq

class NewUserNotificationServicesSaga:
    def __init__(self):
        self.queue_name = os.getenv('RABBIT_QUEUE_NEW_USER_NOTIFICATION')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.routing_key = os.getenv('RABBIT_ROUTING_KEY_USER_TOKEN')
        self.logger = logging.getLogger(__name__)

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
            self.logging.info('New User queue is ready to consume messages...') 
        except Exception as e:
            self.logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        self.logging.info(f'Received message: {request}')
        email = self.user_repository.get_user_by_id(request['email'])
        self.notification_service.send_notification(email, request['token'])
        self.logging.info(f'Notification sent to user: {email}')
        ch.basic_ack(delivery_tag=method.delivery_tag)