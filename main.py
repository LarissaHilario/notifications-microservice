from fastapi import FastAPI
from notifications.infrastructure.dependencies import init_queues
from notifications.infrastructure.routers.notification_router import init_routers_notifications
from database.database import DBConnection
from notifications.infrastructure.repositories.repository_notification import (
    NotificationRepository,
)
from notifications.infrastructure.repositories.notification_model import (
    ModelNotification,
)
import logging, sys, os

logging.getLogger("pika").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)
db_connection = DBConnection()
model_notification = ModelNotification()
notification_repository = NotificationRepository(model_notification)

app = FastAPI()

init_routers_notifications(app)


if __name__ == "__main__":
    import uvicorn
    logging.info(f'API is running')
    try:
        init_queues()
        uvicorn.run(app, host="0.0.0.0", port=3002)
    except Exception as e:
        logging.error(f'Error while running API: {str(e)}')
    except KeyboardInterrupt:
        logging.warn('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)