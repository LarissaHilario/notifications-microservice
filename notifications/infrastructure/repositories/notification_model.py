from database.database import Base
from sqlalchemy import Column, String


class ModelNotification(Base):
    __tablename__ = "notifications"

    uuid = Column(String(36), primary_key=True)
    title = Column(String(100))
    message = Column(String(255))
    date_sent = Column(String(50))
    user_uuid = Column(String(36))
    type = Column(String(50))

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "message": self.message,
            "date_sent": self.date_sent,
            "user_uuid": self.user_uuid,
            "type": self.type,
        }
