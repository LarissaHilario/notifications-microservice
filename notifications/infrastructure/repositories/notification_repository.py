from notifications.domain.repositories.notification_repository import NotificationsInterface
from notifications.infrastructure.configurations.sns.ses_client_config import ses_client
from dotenv import load_dotenv
from os import getenv
import time

load_dotenv()


class NotificationRepository(NotificationsInterface):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def send_email(self, email: str, message: str, subject: str) -> None:
        response = ses_client.send_email(
            Source=getenv("SES_SOURCE_EMAIL"),
            Destination={
                'ToAddresses': [
                    email,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': message,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

