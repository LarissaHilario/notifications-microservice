import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq

class MemeberPaymentNotificationServicesSaga:
    def __init__(self, email_services):
        self.email_services=email_services
        self.queue_name = os.getenv('RABBIT_QUEUE_MEMBER_PAYMENT_RECEIVE')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.logger = logging.getLogger(__name__)

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
            self.logging.info('Payment memeber queue is ready to consume messages...') 
        except Exception as e:
            self.logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        self.logging.info(f'Received message: {request}')
        email = self.user_repository.get_user_by_id(request['email'])
        product = request['product'] #que estas pagando, pues deberia mostrar aqui que el producto es una membresia
        self.email_services.send_email(email, "Payment", f"Your payment for {product} has been received")
        self.logging.info(f'Notification sent to email:  {email}, product: {product}')
        ch.basic_ack(delivery_tag=method.delivery_tag)