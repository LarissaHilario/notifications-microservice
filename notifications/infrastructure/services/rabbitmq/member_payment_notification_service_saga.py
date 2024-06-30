import json
import logging
from notifications.infrastructure.enums.enum_queues import Queue
from notifications.infrastructure.configurations.rabbitmq.rabbitmq_config import setup_rabbitmq

logging.basicConfig(level=logging.INFO)


class MemberPaymentNotificationServicesSaga:
    def __init__(self, notification_use_case):
        logging.basicConfig(level=logging.INFO)
        self.notification_use_case = notification_use_case
        self.queue_name = Queue.QUEUE_PAYMENT_MEMBER_PACKAGE.value["queue"]
        self.exchange_name = Queue.QUEUE_PAYMENT_MEMBER_PACKAGE.value["exchange"]
        self.routing_key = Queue.QUEUE_PAYMENT_MEMBER_PACKAGE.value["routing_key"]

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
        email = request['email']
        user_uuid = request['userUUID']
        order = request['orderUUID']
        subject = "Payment"
        self.notification_use_case.execute(user_uuid, email, f"Your payment for {order} has been received", subject)
        # email = request['email']
        # product = request['product']  # que estas pagando, pues deberia mostrar aqui que el producto es una membresia
        # self.email_services.send_email(email, "Payment", f"Your payment for {product} has been received")
        # logging.info(f'Notification sent to email:  {email}, product: {product}')
