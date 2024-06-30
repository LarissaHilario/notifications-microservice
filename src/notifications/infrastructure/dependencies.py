import threading
from notifications.infrastructure.services.rabbitmq.arrive_package_notification_service_saga import \
    ArrivePackageNotificationServicesSaga
from notifications.infrastructure.services.rabbitmq.get_user_info_req_services_saga import GetUserInfoReqServicesSaga
from notifications.infrastructure.services.rabbitmq.get_user_info_res_services_saga import GetUserInfoResServicesSaga
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

notification_repository = NotificationRepository(db_connection)

notification_use_case = SendNotificationUseCase(notification_repository)

arrive_package_notification = ArrivePackageNotificationServicesSaga(notification_use_case)
member_payment_notification = MemberPaymentNotificationServicesSaga(notification_use_case)
new_user_notification = NewUserNotificationServicesSaga(notification_use_case)
package_payment_notification = PackagePaymentNotificationServicesSaga(notification_use_case)
get_user_info_res = GetUserInfoResServicesSaga()
get_user_info_req = GetUserInfoReqServicesSaga()
def init_queues():
    threading.Thread(target=arrive_package_notification.execute).start()
    threading.Thread(target=member_payment_notification.execute).start()
    threading.Thread(target=new_user_notification.execute).start()
    threading.Thread(target=package_payment_notification.execute).start()
    threading.Thread(target=get_user_info_res.execute).start()
