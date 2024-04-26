"""Argos agent

Fetchs the tasks from the server, execute it and send the result to the server
"""
import asyncio
import json
import logging
import socket
from typing import List

import httpx
from tenacity import retry, wait_random  # type: ignore

from argos.checks import get_registered_check
from argos.logging import logger
from argos.schemas import AgentResult, SerializableException, Task


def log_failure(retry_state):
    """Log failures, with a different log level depending on the number of attempts."""
    if retry_state.attempt_number < 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    logger.log(
        loglevel,
        "Retrying: attempt %s ended with: %s %s",
        retry_state.attempt_number,
        retry_state.outcome,
        retry_state.outcome.exception(),
    )


class ArgosAgent:
    """The Argos agent is responsible for running the checks and reporting the results."""

    def __init__(self, server: str, auth: str, max_tasks: int, wait_time: int):
        self.server = server
        self.max_tasks = max_tasks
        self.wait_time = wait_time
        self.auth = auth
        self._http_client = None

        self.agent_id = socket.gethostname()

    @retry(after=log_failure, wait=wait_random(min=1, max=2))
    async def run(self):
        headers = {
            "Authorization": f"Bearer {self.auth}",
        }
        self._http_client = httpx.AsyncClient(headers=headers)
        logger.info("Running agent against %s", self.server)
        async with self._http_client:
            while "forever":
                retry_now = await self._get_and_complete_tasks()
                if not retry_now:
                    logger.error("Waiting %i seconds before next retry", self.wait_time)
                    await asyncio.sleep(self.wait_time)

    async def _complete_task(self, task: dict) -> dict:
        try:
            task = Task(**task)
            check_class = get_registered_check(task.check)
            check = check_class(self._http_client, task)
            result = await check.run()
            status = result.status
            context = result.context

        except Exception as err:  # pylint: disable=broad-except
            status = "error"
            context = SerializableException.from_exception(err)
            msg = f"An exception occured when running {task}. {err.__class__.__name__} : {err}"
            logger.error(msg)
        return AgentResult(task_id=task.id, status=status, context=context)

    async def _get_and_complete_tasks(self):
        # Fetch the list of tasks
        response = await self._http_client.get(
            f"{self.server}/api/tasks",
            params={"limit": self.max_tasks, "agent_id": self.agent_id},
        )

        if response.status_code == httpx.codes.OK:
            # XXX Maybe we want to group the tests by URL ? (to issue one request per URL)
            data = response.json()
            logger.info("Received %i tasks from the server", len(data))

            tasks = []
            for task in data:
                tasks.append(self._complete_task(task))

            if tasks:
                results = await asyncio.gather(*tasks)
                await self._post_results(results)
                return True

            logger.error("Got no tasks from the server.")
            return False

        logger.error("Failed to fetch tasks: %s", response.read())
        return False

    async def _post_results(self, results: List[AgentResult]):
        data = [r.model_dump() for r in results]
        response = await self._http_client.post(
            f"{self.server}/api/results", params={"agent_id": self.agent_id}, json=data
        )

        if response.status_code == httpx.codes.CREATED:
            logger.error("Successfully posted results %s", json.dumps(response.json()))
        else:
            logger.error("Failed to post results: %s", response.read())
        return response
