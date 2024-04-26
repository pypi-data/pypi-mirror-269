from datetime import datetime, timedelta

import pytest

from argos import schemas
from argos.server import queries
from argos.server.models import Result, Task


@pytest.mark.asyncio
async def test_remove_old_results(db, ten_tasks):
    for task in ten_tasks:
        for i in range(5):
            result = Result(
                submitted_at=datetime.now(),
                status="success",
                context={"foo": "bar"},
                task=task,
                agent_id="test",
                severity="ok",
            )
            db.add(result)
    db.commit()

    # So we have 5 results per tasks
    assert db.query(Result).count() == 50
    # Keep only 2
    deleted = await queries.remove_old_results(db, 2)
    assert deleted == 30
    assert db.query(Result).count() == 20
    for task in ten_tasks:
        assert db.query(Result).filter(Result.task == task).count() == 2


@pytest.mark.asyncio
async def test_remove_old_results_with_empty_db(db):
    assert db.query(Result).count() == 0
    deleted = await queries.remove_old_results(db, 2)
    assert deleted == 0


@pytest.mark.asyncio
async def test_release_old_locks(db, ten_locked_tasks, ten_tasks):
    assert db.query(Task).count() == 20
    released = await queries.release_old_locks(db, 10)
    assert released == 10


@pytest.mark.asyncio
async def test_release_old_locks_with_empty_db(db):
    assert db.query(Task).count() == 0
    released = await queries.release_old_locks(db, 10)
    assert released == 0


@pytest.mark.asyncio
async def test_update_from_config_with_duplicate_tasks(db, empty_config):
    # We pass the same path twice
    fake_path = dict(path="/", checks=[{"body-contains": "foo"}])
    website = schemas.config.Website(
        domain="https://example.org",
        paths=[
            fake_path,
            fake_path,
        ],
    )
    empty_config.websites = [website]

    assert db.query(Task).count() == 0
    await queries.update_from_config(db, empty_config)

    # Only one path has been saved in the database
    assert db.query(Task).count() == 1

    # Calling again with the same data works, and will not result in more tasks being
    # created.
    await queries.update_from_config(db, empty_config)


@pytest.mark.asyncio
async def test_update_from_config_db_can_remove_duplicates_and_old_tasks(
    db, empty_config, task
):
    # Add a duplicate in the db
    same_task = Task(
        url=task.url,
        domain=task.domain,
        check=task.check,
        expected=task.expected,
        frequency=task.frequency,
    )
    db.add(same_task)
    db.commit()
    assert db.query(Task).count() == 2

    website = schemas.config.Website(
        domain=task.domain,
        paths=[
            dict(
                path="https://another-example.com", checks=[{task.check: task.expected}]
            ),
            dict(path=task.url, checks=[{task.check: task.expected}]),
        ],
    )
    empty_config.websites = [website]

    await queries.update_from_config(db, empty_config)
    assert db.query(Task).count() == 2

    website = schemas.config.Website(
        domain=task.domain,
        paths=[
            dict(
                path="https://another-example.com", checks=[{task.check: task.expected}]
            ),
        ],
    )
    empty_config.websites = [website]

    await queries.update_from_config(db, empty_config)
    assert db.query(Task).count() == 1


@pytest.mark.asyncio
async def test_update_from_config_db_updates_existing_tasks(db, empty_config, task):
    assert db.query(Task).count() == 1

    website = schemas.config.Website(
        domain=task.domain,
        paths=[
            dict(path=task.url, checks=[{task.check: task.expected}]),
        ],
    )
    empty_config.websites = [website]

    await queries.update_from_config(db, empty_config)
    assert db.query(Task).count() == 1


@pytest.mark.asyncio
async def test_reschedule_all(
    db, ten_tasks, ten_warning_tasks, ten_critical_tasks, ten_ok_tasks
):
    assert db.query(Task).count() == 40
    assert db.query(Task).filter(Task.severity == "unknown").count() == 10
    assert db.query(Task).filter(Task.severity == "warning").count() == 10
    assert db.query(Task).filter(Task.severity == "critical").count() == 10
    assert db.query(Task).filter(Task.severity == "ok").count() == 10

    one_hour_ago = datetime.now() - timedelta(hours=1)
    assert db.query(Task).filter(Task.next_run <= one_hour_ago).count() == 0

    await queries.reschedule_all(db)
    assert db.query(Task).filter(Task.next_run <= one_hour_ago).count() == 30


@pytest.fixture
def task(db):
    task = Task(
        url="https://www.example.com",
        domain="https://www.example.com",
        check="body-contains",
        expected="foo",
        frequency=1,
    )
    db.add(task)
    db.commit()
    return task


@pytest.fixture
def empty_config():
    return schemas.config.Config(
        general=schemas.config.General(
            frequency="1m",
            alerts=schemas.config.Alert(
                ok=["", ""],
                warning=["", ""],
                critical=["", ""],
                unknown=["", ""],
            ),
        ),
        service=schemas.config.Service(
            secrets=[
                "1234",
            ]
        ),
        ssl=schemas.config.SSL(thresholds=[]),
        websites=[],
    )


@pytest.fixture
def ten_results(db, task):
    results = []
    for i in range(10):
        result = Result(
            submitted_at=datetime.now(),
            status="success",
            context={"foo": "bar"},
            task=task,
            agent_id="test",
            severity="ok",
        )
        db.add(result)
        results.append(result)
    db.commit()
    return results


@pytest.fixture
def ten_locked_tasks(db):
    a_minute_ago = datetime.now() - timedelta(minutes=1)
    tasks = []
    for i in range(10):
        task = Task(
            url="https://www.example.com",
            domain="example.com",
            check="body-contains",
            expected="foo",
            frequency=1,
            selected_by="test",
            selected_at=a_minute_ago,
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    return tasks


@pytest.fixture
def ten_tasks(db):
    now = datetime.now()
    tasks = []
    for i in range(10):
        task = Task(
            url="https://www.example.com",
            domain="example.com",
            check="body-contains",
            expected="foo",
            frequency=1,
            selected_by="test",
            selected_at=now,
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    return tasks


@pytest.fixture
def ten_warning_tasks(db):
    now = datetime.now()
    tasks = []
    for i in range(10):
        task = Task(
            url="https://www.example.com",
            domain="example.com",
            check="body-contains",
            expected="foo",
            frequency=1,
            next_run=now,
            severity="warning",
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    return tasks


@pytest.fixture
def ten_critical_tasks(db):
    now = datetime.now()
    tasks = []
    for i in range(10):
        task = Task(
            url="https://www.example.com",
            domain="example.com",
            check="body-contains",
            expected="foo",
            frequency=1,
            next_run=now,
            severity="critical",
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    return tasks


@pytest.fixture
def ten_ok_tasks(db):
    now = datetime.now()
    tasks = []
    for i in range(10):
        task = Task(
            url="https://www.example.com",
            domain="example.com",
            check="body-contains",
            expected="foo",
            frequency=1,
            next_run=now,
            severity="ok",
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    return tasks
