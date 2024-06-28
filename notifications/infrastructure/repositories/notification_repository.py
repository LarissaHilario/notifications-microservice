from notifications.domain.repositories.notification_repository import NotificationsInterface
from notifications.infrastructure.configurations.sns.sns_client_config import sns_client
from dotenv import load_dotenv
from os import getenv
import time

load_dotenv()


class NotificationRepository(NotificationsInterface):
    def _init_(self, db_connection):
        self.db_connection = db_connection

    def send_email(self, email: str, message: str, subject: str) -> None:

        topic_arn = getenv("SNS_TOPIC_ARN")

        is_subscribed = False

        paginator = sns_client.get_paginator('list_subscriptions_by_topic')
        for page in paginator.paginate(TopicArn=topic_arn):
            for subscription in page['Subscriptions']:
                if subscription['Endpoint'] == email:
                    is_subscribed = True

        if not is_subscribed:
            response = sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol="email",
                Endpoint=email,
                ReturnSubscriptionArn=True
            )
            time.sleep(50)

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )

        # sns_client.unsubscribe(
        #     SubscriptionArn=subscription_arn
        # )

