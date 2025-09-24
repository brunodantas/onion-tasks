"""
Abstract interfaces for the use cases layer
implementing the Dependency Inversion Principle.
"""

from typing import List


class TaskRepository:
    def add(self, task) -> None:
        raise NotImplementedError

    def get(self, task_id: str):
        raise NotImplementedError

    def list(self) -> List:
        raise NotImplementedError


class AgentRepository:
    def add(self, agent) -> None:
        raise NotImplementedError

    def get(self, agent_id: str):
        raise NotImplementedError

    def list(self) -> list:
        raise NotImplementedError


class ProjectRepository:
    def add(self, project) -> None:
        raise NotImplementedError

    def get(self, project_id: str):
        raise NotImplementedError

    def list(self) -> list:
        raise NotImplementedError
    
