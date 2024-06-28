from fastapi import APIRouter, HTTPException
from os import getenv
from dotenv import load_dotenv

from notifications.application.useCases.send_notification_use_case import SendNotificationUseCase
from notifications.infrastructure.repositories.notification_repository import NotificationRepository
from notifications.infrastructure.utilities.formatters import formatter_message

load_dotenv()

routes = APIRouter()

notification_repository = NotificationRepository("DB")

notification_use_case = SendNotificationUseCase(notification_repository)


@routes.get("/health")
async def root():
    return {"message": "OK"}


@routes.get("/send/email")
async def root():
    email = "kristellperez34@gmail.com"
    email_test = "Test to send email to {customer_name} from {support_email} with number {support_phone}."
    message_formatted = formatter_message(
        email_test, "User Test",
        getenv("SNS_EMAIL_SUPPORT"),
        getenv("SNS_PHONE_NUMBER_SUPPORT")
    )
    subject = "Test to send email to user"
    try:
        notification_use_case.execute(email, message_formatted, subject)
        base_response = {
            "data": None,
            "message": "Email send successfully",
            "status": True,
            "status_code": 200,
            "http_status": "OK"
        }
    except Exception as e:
        base_response = {
            "data": None,
            "message": str(e),
            "status": False,
            "status_code": 500,
            "http_status": "Internal Server Error"
        }

    return base_response

