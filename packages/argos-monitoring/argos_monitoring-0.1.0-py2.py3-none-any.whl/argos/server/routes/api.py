"""Web interface for machines"""
from typing import List, Union

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from argos.logging import logger
from argos.schemas import AgentResult, Config, Task
from argos.server import queries
from argos.server.alerting import handle_alert
from argos.server.routes.dependencies import get_config, get_db, verify_token

route = APIRouter()


@route.get("/tasks", response_model=list[Task], dependencies=[Depends(verify_token)])
async def read_tasks(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 10,
    agent_id: Union[None, str] = None,
):
    """Return a list of tasks to execute"""
    agent_id = agent_id or request.client.host
    tasks = await queries.list_tasks(db, agent_id=agent_id, limit=limit)
    return tasks


@route.post("/results", status_code=201, dependencies=[Depends(verify_token)])
async def create_results(
    request: Request,
    results: List[AgentResult],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    config: Config = Depends(get_config),
    agent_id: Union[None, str] = None,
):
    """Get the results from the agents and store them locally.

    - Finalize the checks (some checks need the server to do some part of the validation,
      for instance because they need access to the configuration)
    - If it's an error, determine its severity ;
    - Trigger the reporting calls
    """
    agent_id = agent_id or request.client.host
    db_results = []
    for agent_result in results:
        # XXX Maybe offload this to a queue.
        # XXX Get all the tasks at once, to limit the queries on the db
        task = await queries.get_task(db, agent_result.task_id)
        if not task:
            logger.error("Unable to find task %i", agent_result.task_id)
        else:
            last_severity = task.severity
            result = await queries.create_result(db, agent_result, agent_id)
            check = task.get_check()
            status, severity = await check.finalize(config, result, **result.context)
            result.set_status(status, severity)
            task.set_times_severity_and_deselect(severity, result.submitted_at)

            # Don’t create an alert if the severity has not changed
            if last_severity != severity:
                background_tasks.add_task(
                    handle_alert, config, result, task, severity, last_severity, request
                )

            db_results.append(result)
    db.commit()
    return {"result_ids": [r.id for r in db_results]}


@route.post(
    "/reschedule/all",
    responses={
        200: {
            "content": {
                "application/json": {"example": {"msg": "Non OK tasks reschuled"}}
            }
        }
    },
)
async def reschedule_all(request: Request, db: Session = Depends(get_db)):
    """Reschedule checks of all non OK tasks ASAP"""
    await queries.reschedule_all(db)
    return {"msg": "Non OK tasks reschuled"}


@route.get(
    "/stats",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "upcoming_tasks_count": 0,
                        "results_count": 1993085,
                        "selected_tasks_count": 1845,
                    }
                }
            }
        }
    },
)
async def get_stats(db: Session = Depends(get_db)):
    """Get tasks statistics"""
    return {
        "upcoming_tasks_count": await queries.count_tasks(db, selected=False),
        "results_count": await queries.count_results(db),
        "selected_tasks_count": await queries.count_tasks(db, selected=True),
    }


@route.get(
    "/severities",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"ok": 1541, "warning": 0, "critical": 0, "unknown": 0}
                }
            }
        }
    },
)
async def get_severity_counts(db: Session = Depends(get_db)):
    """Returns the number of results per severity"""
    return await queries.get_severity_counts(db)
