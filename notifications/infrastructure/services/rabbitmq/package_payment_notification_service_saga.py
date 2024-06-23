import json
import logging
from notifications.infrastructure.enums.enum_queues import Queue
from notifications.infrastructure.configurations.rabbitmq.rabbitmq_config import setup_rabbitmq

logging.basicConfig(level=logging.INFO)


class PackagePaymentNotificationServicesSaga:
    def __init__(self, notification_use_case):
        logging.basicConfig(level=logging.INFO)
        self.notification_use_case = notification_use_case
        self.queue_name = Queue.QUEUE_PAYMENT_PACKAGE.value["queue"]
        self.exchange_name = Queue.QUEUE_PAYMENT_PACKAGE.value["exchange"]
        self.routing_key = Queue.QUEUE_PAYMENT_PACKAGE.value["routing_key"]

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {str(e)}')

    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        logging.info(f'Received message: {request}')
        email = request['data']['email']
        package_uuid = request['data']['package_uuid']
        subject = "Payment"
        self.notification_use_case.execute(email, f"Your payment for package {package_uuid} has been received", subject)
        # email = request['email']
        # package_uuid = request['package_uuid']
        # payment_uuid = request['payment_uuid']
        # # TODO: hablar con el equipo de paquetes para saber que cosas tiene el objeto paquete response, devolver en la llamada el identificador del paquete y decir que ya esta en camino
        # self.email_services.send_email(email, "Payment", f"Your payment for package {package_uuid} has been received")
        # logging.info(f'Notification sent to email:  {email}, package: {package_uuid}')
