import socketio

from risque.common.constants import (
    DEFAULT_RISQUE_SERVER_HOST, DEFAULT_RISQUE_SERVER_PORT,
)
from risque.common.interfaces import RisqueClientInterface, TaskInterface
from risque.common.singleton import SingletonMeta


class RisqueClient(RisqueClientInterface, metaclass=SingletonMeta):

    def __init__(
        self,
        host: str = DEFAULT_RISQUE_SERVER_HOST,
        port: int = DEFAULT_RISQUE_SERVER_PORT,
    ) -> None:
        self.host = host
        self.port = port
        self.io = socketio.SimpleClient()

        self.io.connect(f"http://{self.host}:{self.port}")

    def queue_task(self, task_request: TaskInterface = None):
        self.io.call(
            "queue_task",
            task_request.to_dict()
        )
