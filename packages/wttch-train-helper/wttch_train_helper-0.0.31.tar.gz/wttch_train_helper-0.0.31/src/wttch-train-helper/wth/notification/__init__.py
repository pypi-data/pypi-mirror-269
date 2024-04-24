from abc import abstractmethod

from .base import BaseNotification


class App:
    """
    为了发送异常信息。
    """

    def __init__(self, notification: BaseNotification, name: str = ""):
        self.notification = notification
        self.name = ""

    def start(self):
        try:
            self._run()
        except Exception as e:
            self.notification.send_text(f"应用[{self.name}]出现异常: {str(e)}")
            raise e

    @abstractmethod
    def _run(self):
        pass
