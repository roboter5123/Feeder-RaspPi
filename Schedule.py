from Task import Task as Task


class Schedule:
    scheduleId: int
    name: str
    tasks: list[Task]

    def __init__(self, schedule_id: int = None, name: str = None, tasks: list[Task] = None) -> None:

        self.scheduleId = schedule_id
        self.name = name
        self.tasks = tasks

    def to_dict(self) -> dict[str, any]:

        return self.__dict__

    def add_task(self, task: Task):

        if self.tasks is None:
            self.tasks = []

        self.tasks.append(task)

    def remove_task(self, task: Task):

        if self.tasks is None:
            self.tasks = []
            return

        if self.tasks.count(task):
            self.tasks.remove(task)

    def to_json(self):

        tasks = []

        for task in self.tasks:
            tasks.append(task.toJson())

        this_json = {"scheduleId": self.scheduleId, "name": self.name, "tasks": tasks}
        return this_json
