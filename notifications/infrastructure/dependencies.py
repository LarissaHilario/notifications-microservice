from notifications.infrastructure.services.arrive_package_notification_services_saga import ArrivePackageNotificationServicesSaga
from notifications.infrastructure.services.email_notification_services import EmailService
from notifications.infrastructure.services.member_payment_notification_services_saga import MemeberPaymentNotificationServicesSaga
from notifications.infrastructure.services.new_user_notification_services_saga import NewUserNotificationServicesSaga
from notifications.infrastructure.services.package_payment_notification_services_saga import PackagePaymentNotificationServicesSaga

email_services = EmailService()
arrive_package_notification = ArrivePackageNotificationServicesSaga(email_services)
member_payment_notification = MemeberPaymentNotificationServicesSaga(email_services)
new_user_notification = NewUserNotificationServicesSaga(email_services)
package_payment_notification = PackagePaymentNotificationServicesSaga(email_services)

def init_queues():
    arrive_package_notification.execute()
    member_payment_notification.execute()
    new_user_notification.execute()
    package_payment_notification.execute()