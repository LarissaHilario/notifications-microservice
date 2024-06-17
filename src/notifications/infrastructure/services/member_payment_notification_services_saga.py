import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq
logging.basicConfig(level=logging.INFO)

class MemeberPaymentNotificationServicesSaga:
    def __init__(self, email_services):
        logging.basicConfig(level=logging.INFO)
        self.email_services=email_services
        self.queue_name = os.getenv('RABBIT_QUEUE_MEMBER_PAYMENT_RECEIVE')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.routing_key = os.getenv('RABBIT_ROUTING_KEY_MEMBER_PAYMENT_RECEIVE')

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            logging.info('Payment memeber queue is ready to consume messages...') 
            channel.start_consuming()
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        logging.info(f'Received message: {request}')
        email = request['email']
        product = request['product'] #que estas pagando, pues deberia mostrar aqui que el producto es una membresia
        self.email_services.send_email(email, "Payment", f"Your payment for {product} has been received")
        logging.info(f'Notification sent to email:  {email}, product: {product}')
