from collections import deque

from risque.common.interfaces import TaskInterface, TaskManagerInterface


class TaskManager(TaskManagerInterface):

    def __init__(self) -> None:
        self.tasks = {}

    def add_task(self, task: TaskInterface = None):
        if task is None:
            return

        if task.kind not in self.tasks:
            self.tasks[task.kind] = deque()

        self.tasks[task.kind].append(task)
        print(self)

    def __repr__(self) -> str:
        task_count = sum(map(
            len,
            self.tasks.values()
        ))
        return f"<TaskManager - task count:{task_count}>"
