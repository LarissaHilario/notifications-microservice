from ..controllers.controller_test import routes as routes_test
from ..controllers.controller_notification import routes as routes_notification


def init_routers_notifications(app):
    app.include_router(routes_test, prefix='/api/v1')
    app.include_router(routes_notification, prefix='/api/v1')
