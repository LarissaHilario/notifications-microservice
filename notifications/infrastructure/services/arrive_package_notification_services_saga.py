import os
import json
import logging
from notifications.infrastructure.config.rabbit_config import setup_rabbitmq

class ArrivePackageNotificationServicesSaga:
    def __init__(self):
        self.queue_name = os.getenv('RABBIT_QUEUE_PACKAGE_ARRIVE')
        self.exchange_name = os.getenv('RABBIT_EXCHANGE_NOTIFICATION')
        self.logger = logging.getLogger(__name__)

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
            self.logging.info('Package arrive queue is ready to consume messages...') 
        except Exception as e:
            self.logging.error(f'Error while consuming message, New User queue: {str(e)}')
            
    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        self.logging.info(f'Received message: {request}')
        email = self.user_repository.get_user_by_id(request['email'])
        package_uuid = request['package_uuid']
        # TODO: hablar con el equipo de paquetes para saber que cosas tiene el objeto paquete response, devolver en la llamada el identificador del paquete y decir que ya esta en camino
        self.notification_service.send_notification(email, package_uuid)
        self.logging.info(f'Notification sent to email:  {email}, package: {package_uuid}')
        ch.basic_ack(delivery_tag=method.delivery_tag)