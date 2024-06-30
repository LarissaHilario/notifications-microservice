
from notifications.infrastructure.controllers.controller_notification import routes as routes_notification


def init_routers_notifications(app):
    app.include_router(routes_notification, prefix='/notifications/api/v1')
