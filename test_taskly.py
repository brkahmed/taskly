import pytest
from taskly import (
    load_database,
    add_task,
    update_task,
    delete_task,
    mark_in_progress_task,
    mark_done_task,
)

DATABASE_PATH: str = "test.json"
database: dict[str, dict] = load_database(DATABASE_PATH)


def test_add_task() -> None:
    add_task(database, "hello, world")
    assert len(database) == 1 and database["1"]["description"] == "hello, world"
    add_task(database, "hi mom")
    add_task(database, "This is CS50")
    add_task(database, "Suiiiiii")
    assert len(database) == 4 and database["3"]["description"] == "This is CS50"


def test_update_task() -> None:
    update_task(database, "1", "goodbye, world")
    assert database["1"]["description"] == "goodbye, world"
    with pytest.raises(KeyError):
        update_task(database, 3, "Error")
    with pytest.raises(KeyError):
        update_task(database, "0", "Error")


def test_mark_in_progress_task() -> None:
    mark_in_progress_task(database, "2")
    assert database["2"]["status"] == "in-progress"
    with pytest.raises(KeyError):
        mark_in_progress_task(database, 6)
    with pytest.raises(KeyError):
        mark_in_progress_task(database, "58")


def test_mark_done_task() -> None:
    mark_done_task(database, "3")
    assert database["3"]["status"] == "done"
    with pytest.raises(KeyError):
        mark_done_task(database, 5)
    with pytest.raises(KeyError):
        mark_done_task(database, "6")


def test_delete_task() -> None:
    delete_task(database, "4")
    assert "4" not in database
    with pytest.raises(KeyError):
        delete_task(database, 5)
    with pytest.raises(KeyError):
        delete_task(database, "4")
