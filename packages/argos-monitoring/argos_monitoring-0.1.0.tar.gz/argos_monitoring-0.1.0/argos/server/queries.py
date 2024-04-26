"""Functions to ease SQL queries management"""
from datetime import datetime, timedelta
from hashlib import sha256
from typing import List
from urllib.parse import urljoin

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from argos import schemas
from argos.logging import logger
from argos.server.models import Result, Task, ConfigCache


async def list_tasks(db: Session, agent_id: str, limit: int = 100):
    """List tasks and mark them as selected"""
    tasks = (
        db.query(Task)
        .filter(
            Task.selected_by == None,  # noqa: E711
            ((Task.next_run <= datetime.now()) | (Task.next_run == None)),  # noqa: E711
        )
        .limit(limit)
        .all()
    )

    now = datetime.now()
    for task in tasks:
        task.selected_at = now
        task.selected_by = agent_id
    db.commit()
    return tasks


async def get_task(db: Session, task_id: int) -> Task:
    return db.get(Task, task_id)


async def create_result(db: Session, agent_result: schemas.AgentResult, agent_id: str):
    result = Result(
        submitted_at=datetime.now(),
        status=agent_result.status,
        context=agent_result.context,
        task_id=agent_result.task_id,
        agent_id=agent_id,
    )
    db.add(result)
    return result


async def count_tasks(db: Session, selected=False):
    query = db.query(Task)
    if selected:
        query = query.filter(Task.selected_by is not None)
    else:
        query = query.filter(Task.selected_by is None)

    return query.count()


async def count_results(db: Session):
    return db.query(Result).count()


async def has_config_changed(db: Session, config: schemas.Config) -> bool:
    """Check if websites config has changed by using a hashsum and a config cache"""
    websites_hash = sha256(str(config.websites).encode()).hexdigest()
    conf_caches = db.query(ConfigCache).all()
    same_config = True
    if conf_caches:
        for conf in conf_caches:
            match conf.name:
                case "websites_hash":
                    if conf.val != websites_hash:
                        same_config = False
                        conf.val = websites_hash
                        conf.updated_at = datetime.now()
                case "general_frequency":
                    if conf.val != str(config.general.frequency):
                        same_config = False
                        conf.val = config.general.frequency
                        conf.updated_at = datetime.now()

        db.commit()

        if same_config:
            return False

    else:  # no config cache found
        web_hash = ConfigCache(
            name="websites_hash", val=websites_hash, updated_at=datetime.now()
        )
        gen_freq = ConfigCache(
            name="general_frequency",
            val=str(config.general.frequency),
            updated_at=datetime.now(),
        )
        db.add(web_hash)
        db.add(gen_freq)
        db.commit()

    return True


async def update_from_config(db: Session, config: schemas.Config):
    """Update tasks from config file"""
    config_changed = await has_config_changed(db, config)
    if not config_changed:
        return {"added": 0, "vanished": 0}

    max_task_id = (
        db.query(func.max(Task.id).label("max_id")).all()  #  pylint: disable-msg=not-callable
    )[0].max_id
    tasks = []
    unique_properties = []
    seen_tasks: List[int] = []
    for website in config.websites:
        domain = str(website.domain)
        frequency = website.frequency or config.general.frequency

        for p in website.paths:
            url = urljoin(domain, str(p.path))
            for check_key, expected in p.checks:
                # Check the db for already existing tasks.
                existing_tasks = (
                    db.query(Task)
                    .filter(
                        Task.url == url,
                        Task.check == check_key,
                        Task.expected == expected,
                    )
                    .all()
                )
                if existing_tasks:
                    existing_task = existing_tasks[0]
                    seen_tasks.append(existing_task.id)

                    if frequency != existing_task.frequency:
                        existing_task.frequency = frequency
                    logger.debug(
                        "Skipping db task creation for url=%s, "
                        "check_key=%s, expected=%s, frequency=%s.",
                        url,
                        check_key,
                        expected,
                        frequency,
                    )

                else:
                    properties = (url, check_key, expected)
                    if properties not in unique_properties:
                        unique_properties.append(properties)
                        task = Task(
                            domain=domain,
                            url=url,
                            check=check_key,
                            expected=expected,
                            frequency=frequency,
                        )
                        logger.debug("Adding a new task in the db: %s", task)
                        tasks.append(task)

    db.add_all(tasks)
    db.commit()

    # Delete vanished tasks
    if max_task_id:
        vanished_tasks = (
            db.query(Task)
            .filter(Task.id <= max_task_id, Task.id.not_in(seen_tasks))
            .delete()
        )
        db.commit()
        logger.info(
            "%i tasks has been removed since not in config file anymore", vanished_tasks
        )
        return {"added": len(tasks), "vanished": vanished_tasks}

    return {"added": len(tasks), "vanished": 0}


async def get_severity_counts(db: Session) -> dict:
    """Get the severities (ok, warning, critical…) and their count"""
    query = db.query(Task.severity, func.count(Task.id).label("count")).group_by(  # pylint: disable-msg=not-callable
        Task.severity
    )

    # Execute the query and fetch the results
    task_counts_by_severity = query.all()

    counts_dict = dict(task_counts_by_severity)
    for key in ("ok", "warning", "critical", "unknown"):
        counts_dict.setdefault(key, 0)
    return counts_dict


async def reschedule_all(db: Session):
    """Reschedule checks of all non OK tasks ASAP"""
    db.query(Task).filter(Task.severity.in_(["warning", "critical", "unknown"])).update(
        {Task.next_run: datetime.now() - timedelta(days=1)}
    )
    db.commit()


async def remove_old_results(db: Session, max_results: int):
    tasks = db.query(Task).all()
    deleted = 0
    for task in tasks:
        # Get the id of the oldest result to keep
        subquery = (
            db.query(Result.id)
            .filter(Result.task_id == task.id)
            .order_by(desc(Result.id))
            .limit(max_results)
            .subquery()
        )
        min_id = db.query(func.min(subquery.c.id)).scalar()  #  pylint: disable-msg=not-callable

        # Delete all the results older than min_id
        if min_id:
            deleted += (
                db.query(Result)
                .where(Result.id < min_id, Result.task_id == task.id)
                .delete()
            )
            db.commit()

    return deleted


async def release_old_locks(db: Session, max_lock_seconds: int):
    """Remove outdated locks on tasks"""
    max_acceptable_time = datetime.now() - timedelta(seconds=max_lock_seconds)

    # Release the locks on jobs that have been selected_at for more than max_lock_time
    updated = (
        db.query(Task)
        .filter(Task.selected_at < max_acceptable_time)
        .update({Task.selected_at: None, Task.selected_by: None})
    )
    db.commit()
    return updated
