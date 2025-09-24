"""
Test suite for use cases layer.
"""

from use_cases import dtos, interfaces, use_cases


class MemoryTaskRepository(interfaces.TaskRepository):
    def __init__(self):
        self.storage = {}

    def add(self, task) -> None:
        task_id = len(self.storage) + 1
        task["task_id"] = str(task_id)
        self.storage[task["task_id"]] = task

    def get(self, task_id: str):
        if task_id in self.storage:
            return self.storage[task_id]
        return None

    def list(self) -> list:
        return list(self.storage.values())


class MemoryAgentRepository(interfaces.AgentRepository):
    def __init__(self):
        self.storage = {}

    def add(self, agent) -> None:
        agent_id = len(self.storage) + 1
        agent["agent_id"] = str(agent_id)
        self.storage[agent["agent_id"]] = agent

    def get(self, agent_id: str):
        if agent_id in self.storage:
            return self.storage[agent_id]
        return None

    def list(self) -> list:
        return list(self.storage.values())


def test_create_task():
    repository = MemoryTaskRepository()
    result = use_cases.create_task(
        repository,
        title="Test Task",
        description="A test task",
        cost=5,
        tags=["MEDIUM_PRIORITY"],
    )
    assert isinstance(result, dtos.Success)
    task = result.value
    assert isinstance(task, dict)
    assert task["title"] == "Test Task"
    assert task["description"] == "A test task"
    assert task["cost"] == 5
    assert task["tags"] == ["MEDIUM_PRIORITY"]
    assert task["status"] == "TODO"
    assert task["task_id"] == "1"


def test_create_task_invalid_cost():
    repository = MemoryTaskRepository()
    result = use_cases.create_task(
        repository,
        title="Invalid Task",
        description="This task has invalid cost",
        cost=0,  # Invalid cost
        tags=["LOW_PRIORITY"],
    )
    assert isinstance(result, dtos.Failure)
    assert "Enterprise rule violation" in result.error


def test_get_task():
    repository = MemoryTaskRepository()
    use_cases.create_task(
        repository,
        title="Test Task",
        description="A test task",
        cost=5,
        tags=["MEDIUM_PRIORITY"],
    )
    result = use_cases.get_task(repository, "1")
    assert isinstance(result, dtos.Success)
    task = result.value
    assert isinstance(task, dict)
    assert task is not None
    assert task["title"] == "Test Task"
    assert task["description"] == "A test task"
    assert task["cost"] == 5
    assert task["tags"] == ["MEDIUM_PRIORITY"]
    assert task["task_id"] == "1"


def test_get_nonexistent_task():
    repository = MemoryTaskRepository()
    result = use_cases.get_task(repository, "999")
    assert isinstance(result, dtos.Failure)
    assert result.error == "Task not found"


def test_assign_task():
    repository = MemoryTaskRepository()
    agent_repository = MemoryAgentRepository()
    task_result = use_cases.create_task(
        repository,
        title="Assignable Task",
        description="A task to be assigned",
        cost=3,
        tags=["LOW_PRIORITY"],
    )
    agent_result = use_cases.create_agent(agent_repository, "agent_123")
    assert isinstance(task_result, dtos.Success) and isinstance(task_result.value, dict)
    assert isinstance(agent_result, dtos.Success) and isinstance(agent_result.value, dict)
    result = use_cases.assign_task(
        repository,
        agent_repository,
        task_result.value["task_id"],
        agent_result.value["agent_id"],
    )
    assert isinstance(result, dtos.Success)
