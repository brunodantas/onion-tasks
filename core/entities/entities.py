"""
Core entities module.
This is the highest level of abstraction in the project,
and has no dependencies on other modules.

This could be split into multiple files if it grows too large.

> Entities encapsulate Enterprise wide business rules.
"""

from collections import Counter
from enum import Enum
from typing import Dict, List


class Status(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class Tag(Enum):
    HIGH_PRIORITY = "High Priority"
    MEDIUM_PRIORITY = "Medium Priority"
    LOW_PRIORITY = "Low Priority"


class Task:
    def __init__(
        self,
        task_id: str | None,
        title: str,
        description: str = "",
        cost: int = 1,
        status: Status = Status.TODO,
        tags=[],
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.cost = cost
        self.status = status
        self.tags = tags
        self.dependencies = set()
        self.project = None
        self.assignee = None

        if cost < 1:
            raise ValueError("Cost must be at least 1")

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status.name}, description={self.description})"

    def add_dependency(self, task: "Task") -> None:
        """
        Add a dependency to the task.

        :param self: The task to which the dependency is being added
        :param task: The task that is being added as a dependency
        :type task: "Task"
        """
        self.dependencies.add(task)
        if not validate_dependencies(self):
            self.dependencies.remove(task)

    def can_start(self) -> bool:
        """
        Check if the task can be started based on its dependencies.
        A task can be started if all its dependencies are marked as DONE.

        :param self: The task to check
        :return: True if the task can be started, False otherwise
        :rtype: bool
        """
        return self.assignee is not None and (
            not self.dependencies
            or all(dep.status == Status.DONE for dep in self.dependencies)
        )

    def start_task(self) -> bool:
        """
        Start the task if all dependencies are met.

        :param self: The task to start
        :return: True if the task was started, False otherwise
        :rtype: bool
        """
        if self.can_start():
            self.status = Status.IN_PROGRESS
            return True
        return False

    def can_complete(self) -> bool:
        """
        Check if the task can be marked as DONE.
        A task can be marked as DONE if it is currently IN_PROGRESS.

        :param self: The task to check
        :return: True if the task can be marked as DONE, False otherwise
        :rtype: bool
        """
        return self.status == Status.IN_PROGRESS

    def complete_task(self) -> bool:
        """
        Mark the task as DONE if it is currently IN_PROGRESS.

        :param self: The task to complete
        :return: True if the task was marked as DONE, False otherwise
        :rtype: bool
        """
        if self.can_complete():
            self.status = Status.DONE
            return True
        return False

    def set_project(self, project: "Project") -> None:
        """
        Associate the task with a project.

        :param self: The task to associate
        :param project: The project to associate the task with
        :type project: "Project"
        """
        self.project = project

    def assign(self, assignee: "Agent") -> None:
        """
        Assign the task to an agent.

        :param self: The task to assign
        :param assignee: The agent to assign the task to
        :type assignee: "Agent"
        """
        self.assignee = assignee


class Agent:
    def __init__(self, agent_id: str, name: str) -> None:
        self.agent_id = agent_id
        self.name = name

    def __repr__(self):
        return f"Agent(name={self.name})"


class Project:
    def __init__(self, project_id: str, name: str) -> None:
        self.project_id = project_id
        self.name = name

    def __repr__(self):
        return f"Project(name={self.name})"


def validate_dependencies(task: Task) -> bool:
    """
    Validate that the dependencies are not circular
    with a depth-first search.

    :param task: The task to validate
    :type task: Task
    :return: True if the dependencies are valid, False otherwise
    :rtype: bool
    """
    seen = set()
    stack = [task]

    while stack:
        current = stack.pop()
        if current in seen:
            return False
        seen.add(current)
        stack.extend(current.dependencies)
    return True


def get_makespan_boundaries(tasks: List[Task]) -> tuple[int, int]:
    """
    Get the makespan boundaries for a set of tasks and agents.

    :param tasks: The list of tasks to consider
    :type tasks: list[Task]
    :param agent_quantity: The number of agents available
    :type agent_quantity: int
    :return: A tuple containing the minimum and maximum makespan
    :rtype: tuple[int, int]
    """
    if not tasks:
        return (0, 0)
    # Worst case: all tasks in sequence
    max_makespan = sum(
        task.cost for task in tasks
    )

    # Best case: all tasks in parallel
    min_makespan = max(task.cost for task in tasks)

    return (min_makespan, max_makespan)


def track_statuses(tasks: List[Task]) -> Dict[Status, int]:
    """
    Return a dictionary with the count of tasks in each status.

    :param tasks: The list of tasks to track
    :type tasks: List[Task]
    :return: A dictionary with the count of tasks in each status
    :rtype: dict[Status, int]
    """
    return Counter(task.status for task in tasks)
