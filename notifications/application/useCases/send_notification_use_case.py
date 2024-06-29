from notifications.infrastructure.configurations.sns.sns_client_config import sns_client
from dotenv import load_dotenv
from os import getenv
import time
from notifications.domain.entities.notification import Notifications
import datetime
import uuid

load_dotenv()


class SendNotificationUseCase:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def execute(self, uuid_user, email, message, subject, type_notification):
        topic_arn = getenv("SNS_TOPIC_ARN")

        is_subscribed = False
        paginator = sns_client.get_paginator('list_subscriptions_by_topic')
        for page in paginator.paginate(TopicArn=topic_arn):
            for subscription in page['Subscriptions']:
                if subscription['Endpoint'] == email:
                    is_subscribed = True
                    break

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

        notification_uuid = str(uuid.uuid4())
        date_sent = datetime.datetime.now()
        notification = Notifications(uuid=notification_uuid, type=type_notification, title=subject,
                                     message=message, date_sent=date_sent)

        try:
            self.notification_repository.save_data(notification, uuid_user)
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            return False

        return True
