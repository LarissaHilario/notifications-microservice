import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq
logging.basicConfig(level=logging.INFO)

class PackagePaymentNotificationServicesSaga:
    def __init__(self, email_services):
        logging.basicConfig(level=logging.INFO)
        self.email_services=email_services
        self.queue_name = os.getenv('RABBIT_QUEUE_PACKAGE_PAYMENT_RECEIVE')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.routing_key = os.getenv('RABBIT_ROUTING_KEY_PACKAGE_PAYMENT_RECEIVE')

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            logging.info('Payment package queue is ready to consume messages...')
            channel.start_consuming()
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        logging.info(f'Received message: {request}')
        email = self.user_repository.get_user_by_id(request['email'])
        package_uuid = request['package_uuid']
        payment_uuid = request['payment_uuid']
        # TODO: hablar con el equipo de paquetes para saber que cosas tiene el objeto paquete response, devolver en la llamada el identificador del paquete y decir que ya esta en camino
        self.email_services.send_email(email, "Payment", f"Your payment for package {package_uuid} has been received")
        logging.info(f'Notification sent to email:  {email}, package: {package_uuid}')
        ch.basic_ack(delivery_tag=method.delivery_tag)