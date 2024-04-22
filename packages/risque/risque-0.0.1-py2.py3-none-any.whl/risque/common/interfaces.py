from threading import Lock
from typing import Callable, Deque, Dict, Optional
import socketio
import abc


class SingletonMetaInterface(abc.ABCMeta):

    _instances = {}
    _lock: Lock = Lock()


class TaskInterface(abc.ABC):
    id: Optional[str]
    client_id: str
    kind: str
    data: Dict

    @abc.abstractmethod
    def to_dict(self) -> Dict:
        pass


class TaskManagerInterface(abc.ABC):
    tasks: Dict[str, Deque]

    @abc.abstractmethod
    def add_task(self, task_request: TaskInterface = None):
        pass

    def __repr__(self) -> str:
        pass


class RisqueServerInterface(abc.ABC):
    host: str
    port: int
    io: socketio.AsyncServer
    app: socketio.ASGIApp
    task_manager: TaskManagerInterface

    @abc.abstractmethod
    def register_handlers(
        self,
        event_handler_map: Dict[str, Callable] = None
    ) -> bool:
        pass

    @abc.abstractmethod
    def run(self):
        pass


class RisqueClientInterface(abc.ABC):
    host: str
    port: int
    io: socketio.SimpleClient

    @abc.abstractmethod
    def queue_task(self, task_request: TaskInterface = None):
        pass
