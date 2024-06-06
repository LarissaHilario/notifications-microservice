from fastapi import FastAPI
from notifications.infrastructure.routers.notification_router import init_routers_notifications
from database.database import DBConnection
from notifications.infrastructure.repositories.repository_notification import (
    NotificationRepository,
)
from notifications.infrastructure.repositories.notification_model import (
    ModelNotification,
)

app = FastAPI()

init_routers_notifications(app)

if __name__ == "__main__":
    db_connection = DBConnection()
    model_notification = ModelNotification()
    notification_repository = NotificationRepository(model_notification)
