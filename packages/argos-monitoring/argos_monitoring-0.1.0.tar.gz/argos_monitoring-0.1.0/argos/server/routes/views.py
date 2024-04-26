"""Web interface for humans"""
from collections import defaultdict
from functools import cmp_to_key
from os import path
from typing import Annotated
from urllib.parse import urlparse

from fastapi import APIRouter, Cookie, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from argos.schemas import Config
from argos.server import queries
from argos.server.models import Result, Task
from argos.server.routes.dependencies import get_config, get_db

route = APIRouter()

current_dir = path.dirname(__file__)
templates = Jinja2Templates(directory=path.join(current_dir, "../templates"))
SEVERITY_LEVELS = {"ok": 1, "warning": 2, "critical": 3, "unknown": 4}


@route.get("/")
async def get_severity_counts_view(
    request: Request,
    db: Session = Depends(get_db),
    auto_refresh_enabled: Annotated[bool, Cookie()] = False,
    auto_refresh_seconds: Annotated[int, Cookie()] = 15,
):
    """Shows the number of results per severity"""
    counts_dict = await queries.get_severity_counts(db)

    agents = db.query(Result.agent_id).distinct().all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "counts_dict": counts_dict,
            "agents": agents,
            "auto_refresh_enabled": auto_refresh_enabled,
            "auto_refresh_seconds": auto_refresh_seconds,
        },
    )


@route.get("/domains")
async def get_domains_view(request: Request, db: Session = Depends(get_db)):
    """Show all tasks and their current state"""
    tasks = db.query(Task).all()

    domains_severities = defaultdict(list)
    domains_last_checks = defaultdict(list)

    for task in tasks:
        domain = urlparse(task.url).netloc
        domains_severities[domain].append(task.severity)
        if task.last_severity_update is not None:
            domains_last_checks[domain] = task.last_severity_update
        else:
            domains_last_checks[domain] = "Waiting to be checked"

    def _max_severity(severities):
        return max(severities, key=SEVERITY_LEVELS.get)

    def _cmp_domains(a, b):
        if SEVERITY_LEVELS[a[1]] < SEVERITY_LEVELS[b[1]]:
            return 1
        if SEVERITY_LEVELS[a[1]] > SEVERITY_LEVELS[b[1]]:
            return -1
        if a[0] > b[0]:
            return 1
        if a[0] < b[0]:
            return -1
        return 0

    domains = [(key, _max_severity(value)) for key, value in domains_severities.items()]
    domains.sort(key=cmp_to_key(_cmp_domains))

    agents = db.query(Result.agent_id).distinct().all()

    return templates.TemplateResponse(
        "domains.html",
        {
            "request": request,
            "domains": domains,
            "last_checks": domains_last_checks,
            "total_task_count": len(tasks),
            "agents": agents,
        },
    )


@route.get("/domain/{domain}")
async def get_domain_tasks_view(
    request: Request, domain: str, db: Session = Depends(get_db)
):
    """Show all tasks attached to a domain"""
    tasks = db.query(Task).filter(Task.domain.contains(f"//{domain}")).all()
    return templates.TemplateResponse(
        "domain.html", {"request": request, "domain": domain, "tasks": tasks}
    )


@route.get("/result/{result_id}")
async def get_result_view(
    request: Request, result_id: int, db: Session = Depends(get_db)
):
    """Show the details of a result"""
    result = db.query(Result).get(result_id)
    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )


@route.get("/task/{task_id}/results")
async def get_task_results_view(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    config: Config = Depends(get_config),
):
    """Show history of a task’s results"""
    results = (
        db.query(Result)
        .filter(Result.task_id == task_id)
        .order_by(Result.submitted_at.desc())  # type: ignore[attr-defined]
        .all()
    )
    task = db.query(Task).get(task_id)
    description = task.get_check().get_description(config)
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": results,
            "task": task,
            "description": description,
        },
    )


@route.get("/agents")
async def get_agents_view(request: Request, db: Session = Depends(get_db)):
    """Show argos agents and the last time the server saw them"""
    last_seen = (
        db.query(Result.agent_id, func.max(Result.submitted_at).label("submitted_at"))
        .group_by(Result.agent_id)
        .all()
    )

    return templates.TemplateResponse(
        "agents.html", {"request": request, "last_seen": last_seen}
    )


@route.post("/refresh")
async def set_refresh_cookies_view(
    request: Request,
    auto_refresh_enabled: Annotated[bool, Form()] = False,
    auto_refresh_seconds: Annotated[int, Form()] = 15,
):
    response = RedirectResponse(
        request.url_for("get_severity_counts_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(key="auto_refresh_enabled", value=auto_refresh_enabled)
    response.set_cookie(key="auto_refresh_seconds", value=int(auto_refresh_seconds))
    return response
