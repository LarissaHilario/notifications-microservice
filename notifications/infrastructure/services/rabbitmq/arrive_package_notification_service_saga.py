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
    def __init__(self, notification_use_case, get_user_info_req, response):
        self.user_response = response
        logging.basicConfig(level=logging.INFO)
        self.notification_use_case = notification_use_case
        self.get_user_info_req = get_user_info_req
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
        self.get_user_info_req.execute(request['clientId'])
        message_formatted = formatter_message(
            FEEDBACK_REQUEST_EMAIL, self.user_response.get_name(),
            getenv("SNS_EMAIL_SUPPORT"),
            getenv("SNS_PHONE_NUMBER_SUPPORT")
        )
        subject = "Cuéntanos tu experiencia con 90-Minutos"
        self.notification_use_case.execute(request['clientId'], self.user_response.get_email(), message_formatted, subject)
