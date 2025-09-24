"""
Repository implementations for the adapter layer.
"""

from use_cases import interfaces
from adapters.persistence import models


class DjangoTaskRepository(interfaces.TaskRepository):
    model = models.Task

    def add(self, task) -> None:
        self.model.objects.create(**task)

    def get(self, task_id: str):
        try:
            return self.model.objects.get(task_id=int(task_id))
        except self.model.DoesNotExist:
            return None

    def list(self) -> list:
        return list(self.model.objects.all())
