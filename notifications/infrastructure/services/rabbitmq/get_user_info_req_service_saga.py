import json
import logging

from notifications.infrastructure.configurations.rabbitmq.rabbitmq_config import setup_rabbitmq
from notifications.infrastructure.enums.enum_queues import Queue


class GetUserInfoReqServiceSaga:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.queue_name = Queue.QUEUE_GET_INFO_USER_REQ.value["queue"]
        self.exchange_name = Queue.QUEUE_GET_INFO_USER_REQ.value["exchange"]
        self.routing_key = Queue.QUEUE_GET_INFO_USER_REQ.value["routing_key"]

    def execute(self, clientUUID):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_publish(queue=self.queue_name, routing_key=self.routing_key, exchange=self.exchange_name,
                                  body=clientUUID)
        except Exception as e:
            logging.error(f'Error while consuming message, New User queue: {str(e)}')
