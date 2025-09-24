"""
Views for the web adapter.
"""

from typing import Dict
from django import http
from django.conf import settings

from adapters.persistence import repositories
from use_cases import use_cases


def get_repositories() -> Dict:
    """
    Retrieve repository instances from settings.

    :return: A dictionary with repository instances
    :rtype: dict
    """
    return {
        "task_repository": repositories.DjangoTaskRepository(),
        # "agent_repository": repositories.DjangoAgentRepository(),
        # "project_repository": repositories.DjangoProjectRepository(),
    }


def health_check(request: http.HttpRequest):
    """
    Health check endpoint.

    :return: A dictionary indicating the service is healthy
    :rtype: dict
    """
    return http.JsonResponse({"status": "ok"})


def create_task(request: http.HttpRequest):
    """
    Create a new task endpoint.

    :param request: The HTTP request containing task data
    :type request: HttpRequest
    :return: A dictionary with the created task details
    :rtype: dict
    """
    task_data = request.POST or {}
    if not task_data:
        return http.JsonResponse({"error": "No task data provided"}, status=400)

    result = use_cases.create_task(
        repository=get_repositories()[settings.TASK_REPOSITORY],
        title=task_data.get("title", ""),
        description=task_data.get("description", ""),
        cost=int(task_data.get("cost", 1)),
        tags=task_data.get("tags", []),
    )
    match result:
        case use_cases.dtos.Success(_):
            return http.JsonResponse({"status": "created"}, status=201)
        case use_cases.dtos.Failure(error):
            return http.JsonResponse({"error": error}, status=400)
