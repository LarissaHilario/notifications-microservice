import json
import logging
from dotenv import load_dotenv
from os import getenv
from notifications.infrastructure.configurations.rabbitmq.rabbitmq_config import setup_rabbitmq
from notifications.infrastructure.constants.message_templates import WELCOME_EMAIL
from notifications.infrastructure.enums.enum_queues import Queue
from notifications.infrastructure.utilities.formatters import formatter_message
from notifications.infrastructure.enums.enum_type import Type

load_dotenv()
logging.basicConfig(level=logging.INFO)


class NewUserNotificationServicesSaga:
    def __init__(self, notification_use_case):
        logging.basicConfig(level=logging.INFO)
        self.notification_use_case = notification_use_case
        self.queue_name = Queue.QUEUE_NEW_USER.value["queue"]
        self.exchange_name = Queue.QUEUE_NEW_USER.value["exchange"]
        self.routing_key = Queue.QUEUE_NEW_USER.value["routing_key"]
        self.message_type = Type.TYPE_WELCOME

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
        uuid_user = request['uud']
        email = request['email']
        name = request['name']
        message_formatted = formatter_message(
            WELCOME_EMAIL, name,
            getenv("SNS_EMAIL_SUPPORT"),
            getenv("SNS_PHONE_NUMBER_SUPPORT")
        )
        subject = "Bienvenido a 90-Minutos"
        self.notification_use_case.execute(
            uuid_user, email, message_formatted, subject)
