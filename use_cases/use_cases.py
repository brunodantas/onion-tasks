"""
Use cases module.
This layer orchestrates the flow of data to and from the entities,
and directs those entities to use their enterprise wide business rules
to achieve the goals of the use case.

Also encapsulates enterprise exception handling
while exposing a functional-programming Result type to the adapters.
This could be split into multiple files if it grows too large.

> The software in this layer contains application specific business rules.
> It encapsulates and implements all of the use cases of the system.
"""

# from collections import defaultdict

from core.entities import entities
from use_cases import dtos, interfaces


def create_task(
    repository: interfaces.TaskRepository,
    title: str,
    description: str = "",
    cost: int = 1,
    tags=["LOW_PRIORITY"],  # Default is a business rule, but not an enterprise rule
) -> dtos.Result:
    """
    Create a new task.

    :param title: Title of the task
    :type title: str
    :param description: Description of the task, defaults to ""
    :type description: str, optional
    :param cost: Cost of the task, defaults to 1
    :type cost: int, optional
    :param tags: Tags associated with the task, defaults to ["low"]
    :type tags: list[str], optional
    :return: The created task
    :rtype: Result
    """
    # Run creation enterprise logic, if any
    try:
        task = entities.Task(
            task_id=None,
            title=title,
            description=description,
            cost=cost,
            tags=[entities.Tag[tag] for tag in tags],
        )
    except ValueError as e:
        return dtos.Failure(error=f"Enterprise rule violation: {e}")
    except Exception as e:
        return dtos.Failure(error=f"Unexpected enterprise error: {e}")

    # Persist the task using the repository
    task_dict = dict(
        title=task.title,
        description=task.description,
        cost=task.cost,
        tags=[task.name for task in task.tags],
        status=task.status.name,
    )
    try:
        repository.add(task_dict)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected adapter error: {e}")
    return dtos.Success(task_dict)


def create_agent(
    repository: interfaces.AgentRepository, name: str
) -> dtos.Result:
    """
    Create a new agent.

    :param repository: The agent repository
    :type repository: interfaces.AgentRepository
    :param name: Name of the agent
    :type name: str
    :return: The created agent or an error if creation fails
    :rtype: Result
    """
    try:
        # Run creation enterprise logic, if any
        agent = entities.Agent(agent_id="", name=name)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected enterprise error: {e}")

    agent_dict = dict(name=agent.name)
    try:
        repository.add(agent_dict)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected adapter error: {e}")
    return dtos.Success(agent_dict)


def get_task(repository: interfaces.TaskRepository, task_id: str) -> dtos.Result:
    """
    Retrieve a task by its ID.

    :param repository: The task repository
    :type repository: interfaces.TaskRepository
    :param task_id: The ID of the task to retrieve
    :type task_id: str
    :return: The retrieved task or an error if not found
    :rtype: Result
    """
    try:
        task = repository.get(task_id)
        if task is None:
            return dtos.Failure(error="Task not found")
        return dtos.Success(task)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected adapter error: {e}")


def get_agent(repository: interfaces.AgentRepository, agent_id: str) -> dtos.Result:
    """
    Retrieve an agent by its ID.

    :param repository: The agent repository
    :type repository: interfaces.AgentRepository
    :param agent_id: The ID of the agent to retrieve
    :type agent_id: str
    :return: The retrieved agent or an error if not found
    :rtype: Result
    """
    try:
        agent = repository.get(agent_id)
        if agent is None:
            return dtos.Failure(error="Agent not found")
        return dtos.Success(agent)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected adapter error: {e}")


def assign_task(
    task_repo: interfaces.TaskRepository,
    agent_repo: interfaces.AgentRepository,
    task_id: str,
    agent_id: str,
) -> dtos.Result:
    """
    Assign a task to an agent.

    :param task_repo: The task repository
    :type task_repo: interfaces.TaskRepository
    :param agent_repo: The agent repository
    :type agent_repo: interfaces.AgentRepository
    :param task_id: The ID of the task to assign
    :type task_id: str
    :param agent_id: The ID of the agent to assign the task to
    :type agent_id: str
    :return: The updated task or an error if assignment fails
    :rtype: Result
    """
    try:
        task = task_repo.get(task_id)
        if task is None:
            return dtos.Failure(error="Task not found")

        agent = agent_repo.get(agent_id)
        if agent is None:
            return dtos.Failure(error="Agent not found")

        # Run enterprise rules
        task_entity = entities.Task(
            task_id=task_id,
            title=task["title"],
            description=task.get("description", ""),
            cost=task.get("cost", 1),
            tags=[entities.Tag[tag] for tag in task.get("tags", ["LOW_PRIORITY"])],
            status=entities.Status[task.get("status", "TODO")],
        )
        agent_entity = entities.Agent(agent_id=agent_id, name=agent["name"])
        task_entity.assign(agent_entity)
        result_task = dict(
            task_id=task_entity.task_id,
            title=task_entity.title,
            description=task_entity.description,
            cost=task_entity.cost,
            tags=[tag.name for tag in task_entity.tags],
            status=task_entity.status.name,
            assignee=agent_entity.agent_id,
        )
        task_repo.add(result_task)  # Upsert the task
        return dtos.Success(result_task)
    except Exception as e:
        return dtos.Failure(error=f"Unexpected adapter error: {e}")


# TODO: Implement more use cases as needed, following the same pattern.

# def get_dependencies(
#     repository: interfaces.TaskRepository, task_id: str
# ) -> dtos.Result:
#     """
#     Retrieve the dependencies of a task by its ID.

#     :param repository: The task repository
#     :type repository: interfaces.TaskRepository
#     :param task_id: The ID of the task whose dependencies to retrieve
#     :type task_id: str
#     :return: The list of dependencies or an error if the task is not found
#     :rtype: Result
#     """
#     try:
#         task = repository.get(task_id)
#         if task is None:
#             return dtos.Failure(error="Task not found")
#         dependencies = task.get("dependencies", [])
#         return dtos.Success(dependencies)
#     except Exception as e:
#         return dtos.Failure(error=f"Unexpected adapter error: {e}")


# def get_dependency_graph(
#     repository: interfaces.TaskRepository, task_id: str
# ) -> dtos.Result:
#     """
#     Retrieve the dependency subgraph of a task by its ID.

#     :param repository: The task repository
#     :type repository: interfaces.TaskRepository
#     :param task_id: The ID of the task whose dependency graph to retrieve
#     :type task_id: str
#     :return: The dependency graph or an error if the task is not found
#     :rtype: Result
#     """
#     try:
#         task = repository.get(task_id)
#         if task is None:
#             return dtos.Failure(error="Task not found")
#         graph = defaultdict(list)

#         def dfs(current_task):
#             graph[current_task["task_id"]] = current_task.get("dependencies", [])
#             for dep in current_task.get("dependencies", []):
#                 dfs(dep)

#         dfs(task)
#         return dtos.Success(graph)
#     except Exception as e:
#         return dtos.Failure(error=f"Unexpected adapter error: {e}")
