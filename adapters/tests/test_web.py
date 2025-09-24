"""
Test cases for web adapters.
"""

import pytest
from django import test

from adapters.persistence import repositories
from adapters.web import views


def test_health_check():
    """
    Test health check endpoint
    """
    response = test.Client().get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_no_data():
    """
    Test create task endpoint with no data
    """
    response = test.Client().post("/create-task/", {})
    assert response.status_code == 400
