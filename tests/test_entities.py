"""
Test suite for core entities.
"""

from core.entities import entities


def test_tasks():
    """
    Test task manipulation
    """
    task1 = entities.Task(task_id="1", title="Task 1")
    task2 = entities.Task(task_id="2", title="Task 2")

    assert entities.track_statuses([task1, task2]) == {entities.Status.TODO: 2}

    task1.add_dependency(task2)
    assert task2 in task1.dependencies

    task2.add_dependency(task1)  # This should not create a circular dependency
    assert task1 not in task2.dependencies

    assert task1.can_start() is False
    assert task2.can_start() is False

    task2.assign(entities.Agent(agent_id="a2", name="Agent 2"))
    assert task2.assignee and task2.assignee.agent_id == "a2"

    assert task1.start_task() is False
    assert task2.start_task() is True

    assert entities.track_statuses([task1, task2]) == {
        entities.Status.TODO: 1,
        entities.Status.IN_PROGRESS: 1,
    }

    assert task1.can_complete() is False
    assert task2.can_complete() is True

    assert task2.complete_task() is True

    task1.assign(entities.Agent(agent_id="a1", name="Agent 1"))
    assert task1.can_start()

    assert entities.track_statuses([task1, task2]) == {
        entities.Status.TODO: 1,
        entities.Status.DONE: 1,
    }

    task1.set_project(entities.Project(project_id="p1", name="Project 1"))
    assert task1.project and task1.project.project_id == "p1"

    assert task1.assignee and task1.assignee.agent_id == "a1"


def test_makespan_boundaries():
    """
    Test makespan boundaries
    """
    task1 = entities.Task(task_id="1", title="Task 1", cost=5)
    subtask1 = entities.Task(task_id="2", title="Task 2", cost=10)
    subtask2 = entities.Task(task_id="2", title="Task 2", cost=100)

    task1.add_dependency(subtask1)
    task1.add_dependency(subtask2)

    assert entities.get_makespan_boundaries([task1, subtask1, subtask2]) == (100, 115)
