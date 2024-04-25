import httpx

from systema.notification.base import NotificationBackend


class Ntfy(NotificationBackend):
    def __init__(self, topic: str):
        self.topic = topic
        self.base_url = "https://ntfy.sh/"

    def nofify(self):
        httpx.post("")
