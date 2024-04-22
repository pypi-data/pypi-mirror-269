from functools import partial
from typing import Callable, Dict
import socketio
import uvicorn


from risque.common.constants import (
    DEFAULT_RISQUE_SERVER_HOST, DEFAULT_RISQUE_SERVER_PORT,
)
from risque.common.interfaces import RisqueServerInterface
from risque.common.singleton import SingletonMeta
from risque.server.handlers import server_event_handlers
from risque.task_manager import TaskManager


class RisqueServer(RisqueServerInterface, metaclass=SingletonMeta):

    def __init__(
        self,
        host: str = DEFAULT_RISQUE_SERVER_HOST,
        port: int = DEFAULT_RISQUE_SERVER_PORT,
    ):
        self.host = host
        self.port = port
        self.task_manager = TaskManager()
        self.io = socketio.AsyncServer(async_mode="asgi")
        self.app = socketio.ASGIApp(self.io)

        self.register_handlers(event_handler_map=server_event_handlers)

    def register_handlers(
        self,
        event_handler_map: Dict[str, Callable] = None
    ) -> bool:
        if event_handler_map is None:
            return False

        for event, handler in event_handler_map.items():
            self.io.on(
                event=event,
                handler=partial(handler, server=self)
            )

    def run(self):
        try:
            uvicorn.run(self.app, host=self.host, port=self.port)
        except KeyboardInterrupt:
            pass
