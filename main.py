import uvicorn
from fastapi import FastAPI

from notifications.infrastructure.dependencies import init_queues
from notifications.infrastructure.routers.notification_router import init_routers_notifications

app = FastAPI()

init_routers_notifications(app)


def main():
    init_queues()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
