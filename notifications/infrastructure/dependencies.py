import threading
from notifications.infrastructure.services.rabbitmq.arrive_package_notification_service_saga import \
    ArrivePackageNotificationServicesSaga
from notifications.infrastructure.services.rabbitmq.member_payment_notification_service_saga import \
    MemberPaymentNotificationServicesSaga
from notifications.infrastructure.services.rabbitmq.new_user_notification_service_saga import \
    NewUserNotificationServicesSaga
from notifications.infrastructure.services.rabbitmq.package_payment_notification_service_saga import \
    PackagePaymentNotificationServicesSaga

from database.database import DBConnection
from notifications.infrastructure.repositories.notification_model import ModelNotification

from notifications.infrastructure.repositories.notification_repository import NotificationRepository
from notifications.application.useCases.send_notification_use_case import SendNotificationUseCase

db_connection = DBConnection()
model_notification = ModelNotification()

notification_repository = NotificationRepository(model_notification)

notification_use_case = SendNotificationUseCase(notification_repository)

arrive_package_notification = ArrivePackageNotificationServicesSaga(notification_use_case)
member_payment_notification = MemberPaymentNotificationServicesSaga(notification_use_case)
new_user_notification = NewUserNotificationServicesSaga(notification_use_case)
package_payment_notification = PackagePaymentNotificationServicesSaga(notification_use_case)


def init_queues():
    threading.Thread(target=arrive_package_notification.execute).start()
    threading.Thread(target=member_payment_notification.execute).start()
    threading.Thread(target=new_user_notification.execute).start()
    threading.Thread(target=package_payment_notification.execute).start()
