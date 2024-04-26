import asyncio

import pytest
from fastapi.testclient import TestClient

from argos.schemas import AgentResult, SerializableException
from argos.server import models
from argos.server.queries import update_from_config


def test_read_tasks_requires_auth(app):
    with TestClient(app) as client:
        response = client.get("/api/tasks")
        assert response.status_code == 403


def test_tasks_retrieval_and_results(authorized_client, app):
    asyncio.run(update_from_config(app.state.db, app.state.config))
    with authorized_client as client:
        response = client.get("/api/tasks")
        assert response.status_code == 200

        tasks = response.json()
        assert len(tasks) == 2

        results = []
        for task in tasks:
            results.append(
                AgentResult(task_id=task["id"], status="success", context={})
            )

        data = [r.model_dump() for r in results]
        response = client.post("/api/results", json=data)

        assert response.status_code == 201
        assert app.state.db.query(models.Result).count() == 2

        # The list of tasks should be empty now
        response = client.get("/api/tasks")
        assert len(response.json()) == 0


def test_agents_can_report_errors(authorized_client):
    with authorized_client as client:
        exc = Exception("This is an error")
        serialized_exc = SerializableException.from_exception(exc)
        agent_result = AgentResult(task_id=1, status="error", context=serialized_exc)

        response = client.post(
            "/api/results",
            json=[
                agent_result.model_dump(),
            ],
        )
        assert response.status_code == 201


@pytest.fixture
def ssl_task(db):
    task = models.Task(
        url="https://exemple.com/",
        domain="https://exemple.com/",
        check="ssl-certificate-expiration",
        expected="on-check",
        frequency=1,
    )
    db.add(task)
    db.commit()
    return task


def test_specialized_checks_can_report_errors(authorized_client, ssl_task):
    with authorized_client as client:
        exc = Exception("This is an error")
        serialized_exc = SerializableException.from_exception(exc)
        agent_result = AgentResult(
            task_id=ssl_task.id, status="error", context=serialized_exc
        )

        response = client.post(
            "/api/results",
            json=[
                agent_result.model_dump(),
            ],
        )
        assert response.status_code == 201
