from typing import Any, Dict
from risque.common.interfaces import RisqueServerInterface
from risque.common.task import Task


def on_connect(
    sid: str = None,
    env: Dict = None,
    auth: Any = None,
    server: RisqueServerInterface = None,
):

    print(sid)
    print(server)


def on_queue_task(
    sid: str = None,
    data: Any = None,
    server: RisqueServerInterface = None,
):

    server.task_manager.add_task(Task(**data))


server_event_handlers = {
    "connect": on_connect,
    "queue_task": on_queue_task,
}
