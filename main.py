from fastapi import FastAPI
from notifications.infrastructure.routers.notification_router import init_routers_notifications

app = FastAPI()

init_routers_notifications(app)
