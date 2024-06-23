
class SendNotificationUseCase:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def execute(self, email, message, subject):
        self.notification_repository.send_email(email, message, subject)
