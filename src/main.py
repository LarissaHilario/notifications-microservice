from fastapi import FastAPI
from notifications.infrastructure.dependencies import init_queues
from notifications.infrastructure.repositories.notification_repository import NotificationRepository
from notifications.infrastructure.routers.notification_router import init_routers_notifications
from database.database import DBConnection

from notifications.infrastructure.repositories.notification_model import (
    ModelNotification,
)
import logging, sys, os
import uvicorn


logging.getLogger("pika").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)
db_connection = DBConnection()
model_notification = ModelNotification()
notification_repository = NotificationRepository(model_notification)

app = FastAPI()

init_routers_notifications(app)

def main():
    init_queues()
    logging.info(f'API is running')
    try:
        init_queues()
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logging.error(f'Error while running API: {str(e)}')
    except KeyboardInterrupt:
        logging.warn('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
  main()