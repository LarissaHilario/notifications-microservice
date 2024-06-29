from notifications.domain.repositories.notification_repository import NotificationsInterface
from notifications.domain.entities.notification import Notifications
from .notification_model import ModelNotification


class NotificationRepository(NotificationsInterface):
    def __init__(self, db_connection):
        self.db_session = db_connection.get_session()

    def save_data(self, notification: Notifications, user_id: str):
        data_notification = ModelNotification(
            uuid=notification.uuid,
            type=notification.type,
            title=notification.title,
            message=notification.message,
            date_sent=notification.date_sent,
            user_uuid=user_id
        )
        try:
            self.db_session.add(data_notification)
            self.db_session.commit()
            return True
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            self.db_session.rollback()
            return False
