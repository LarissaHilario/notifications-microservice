import json
import logging
from dotenv import load_dotenv
from os import getenv
from notifications.infrastructure.utilities.formatters import formatter_message
from notifications.infrastructure.configurations.rabbitmq.rabbitmq_config import setup_rabbitmq
from notifications.infrastructure.enums.enum_queues import Queue
from notifications.infrastructure.constants.message_templates import FEEDBACK_REQUEST_EMAIL


load_dotenv()


class ArrivePackageNotificationServicesSaga:
    def __init__(self, notification_use_case):
        logging.basicConfig(level=logging.INFO)
        self.notification_use_case = notification_use_case
        self.queue_name = Queue.QUEUE_ARRIVE_PACKAGE.value["queue"]
        self.exchange_name = Queue.QUEUE_ARRIVE_PACKAGE.value["exchange"]
        self.routing_key = Queue.QUEUE_ARRIVE_PACKAGE.value["routing_key"]

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {e}')

    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        logging.info(f'Received message: {request}')
        email = request['email']
        name = request['name']
        message_formatted = formatter_message(
            FEEDBACK_REQUEST_EMAIL, name,
            getenv("SNS_EMAIL_SUPPORT"),
            getenv("SNS_PHONE_NUMBER_SUPPORT")
        )
        subject = "Cuéntanos tu experiencia con 90-Minutos"
        self.notification_use_case.execute(email, message_formatted, subject)
        # email = request['email']
        # package_uuid = request['package_uuid']
        # TODO: hablar con el equipo de paquetes para saber que cosas tiene el objeto paquete response, devolver en
        #  la llamada el identificador del paquete y decir que ya esta en camino
        # self.email_services.send_email(email, "Arrive package", f"Your package {package_uuid} has arrived")
        # logging.info(f'Notification sent to email:  {email}, package: {package_uuid}')
