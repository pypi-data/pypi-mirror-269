from typing import Dict
from uuid import uuid4

from risque.common.interfaces import TaskInterface


class Task(TaskInterface):

    def __init__(
        self,
        client_id: str = None,
        kind: str = None,
        data: Dict = None,
    ) -> None:
        self.client_id, = client_id,
        self.kind = kind
        self.data = data
        self.id = uuid4().hex

    def to_dict(self) -> Dict:
        return {
            "kind": self.kind,
            "data": self.data,
            "client_id": self.client_id,
        }
