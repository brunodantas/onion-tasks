"""
ORM models for the persistence adapter.
"""

from django.db import models


class Task(models.Model):
    """
    ORM model for Task.
    """

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.IntegerField()
    status = models.CharField(max_length=50)
    assignee = models.ForeignKey(
        "Agent", on_delete=models.SET_NULL, null=True, blank=True
    )
    project = models.ForeignKey(
        "Project", on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.JSONField(default=list)

    def __str__(self):
        return f"Task(id={self.task_id}, title={self.title}, status={self.status})"


class Dependency(models.Model):
    """
    ORM model for Task Dependency.
    """

    task = models.ForeignKey(
        Task, related_name="task_dependencies", on_delete=models.CASCADE
    )
    depends_on = models.ForeignKey(
        Task, related_name="dependent_tasks", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("task", "depends_on")

    def __str__(self):
        return f"Dependency(task_id={self.task.task_id}, depends_on_id={self.depends_on.task_id})"


class Agent(models.Model):
    """
    ORM model for Agent.
    """

    agent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Agent(id={self.agent_id}, name={self.name})"


class Project(models.Model):
    """
    ORM model for Project.
    """

    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Project(id={self.project_id}, name={self.name})"
