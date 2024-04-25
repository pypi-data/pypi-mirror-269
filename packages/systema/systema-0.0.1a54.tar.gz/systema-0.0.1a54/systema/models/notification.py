import enum
from datetime import datetime


class NotificationStatus(str, enum.Enum):
    CREATED = "created"
    POSTED = "posted"


class Notification:
    message: str
    status: NotificationStatus = NotificationStatus.CREATED
    posted_at: datetime | None = None
