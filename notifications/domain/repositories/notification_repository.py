from abc import ABC, abstractmethod
from notifications.domain.entities.notification import Notifications

class NotificationsInterface(ABC):

    @abstractmethod
    def save_data(notification: Notifications) -> Notifications:
        pass
