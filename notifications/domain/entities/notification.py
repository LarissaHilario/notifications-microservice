from dataclasses import dataclass


@dataclass
class Notifications:
    uuid: str
    type: str
    title: str
    message: str
    date_sent: str
