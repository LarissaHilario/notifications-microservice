from abc import ABC, abstractmethod


class NotificationsInterface(ABC):

    @abstractmethod
    def send_email(self, email: str, message: str, subject: str) -> None:
        pass
