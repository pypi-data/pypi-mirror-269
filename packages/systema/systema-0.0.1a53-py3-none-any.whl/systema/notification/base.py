from abc import ABC, abstractmethod


class NotificationBackend(ABC):
    @abstractmethod
    def nofify(self):
        pass
