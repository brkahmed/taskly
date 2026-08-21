from pathlib import Path

import pytest

from taskly import (
    Database,
    add_task,
    delete_task,
    get_date_checker,
    load_database,
    mark_done_task,
    mark_in_progress_task,
    update_task,
)

DATABASE_PATH: str = "test.json"
database: Database = load_database(DATABASE_PATH)


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
        update_task(database, 3, "Error")  # type: ignore
    with pytest.raises(KeyError):
        update_task(database, "0", "Error")
    update_task(database, "1", status="in-progress")
    assert database["1"]["status"] == "in-progress"
    update_task(database, "1")
    assert database["1"]["status"] == "in-progress" and database["1"]["description"] == "goodbye, world"
    with pytest.raises(ValueError):
        update_task(database, "1", status="invalid-status")  # type: ignore


def test_mark_in_progress_task() -> None:
    mark_in_progress_task(database, "2")
    assert database["2"]["status"] == "in-progress"
    with pytest.raises(KeyError):
        mark_in_progress_task(database, 6)  # type: ignore
    with pytest.raises(KeyError):
        mark_in_progress_task(database, "58")


def test_mark_done_task() -> None:
    mark_done_task(database, "3")
    assert database["3"]["status"] == "done"
    with pytest.raises(KeyError):
        mark_done_task(database, 5)  # type: ignore
    with pytest.raises(KeyError):
        mark_done_task(database, "6")


def test_delete_task() -> None:
    delete_task(database, "4")
    assert "4" not in database
    with pytest.raises(KeyError):
        delete_task(database, 5)  # type: ignore
    with pytest.raises(KeyError):
        delete_task(database, "4")


def test_list_task() -> None:
    with pytest.raises(ValueError):
        update_task(database, "1", status="invalid-status")  # type: ignore


def test_date_checker() -> None:
    date_checker = get_date_checker("2008-06-24")
    assert date_checker("2008-06-24T14:30:00.000000")
    assert not date_checker("2008-06-25T14:30:00.000000")

    date_checker = get_date_checker("2008-06")
    assert date_checker("2008-06-24T14:30:00.000000")
    assert date_checker("2008-06-1T14:30:00.000000")
    assert not date_checker("2025-07-1T14:30:00.000000")
    assert not date_checker("2008-05-1T14:30:00.000000")

    date_checker = get_date_checker("2008")
    assert date_checker("2008-06-24T14:30:00.000000")
    assert date_checker("2008-01-01T14:30:00.000000")
    assert not date_checker("2024-12-31T14:30:00.000000")
    assert not date_checker("2026-12-31T14:30:00.000000")

    date_checker = get_date_checker(">2008-06-24")
    assert date_checker("2008-06-24T14:30:00.000000")
    assert date_checker("2025-05-21T14:30:00.000000")
    assert date_checker("2022-06-23T14:30:00.000000")
    assert not date_checker("2001-06-22T14:30:00.000000")

    date_checker = get_date_checker("<2008-06-24")
    assert date_checker("2008-06-24T14:30:00.000000")
    assert date_checker("2002-06-24T14:30:00.000000")
    assert date_checker("2008-06-23T14:30:00.000000")
    assert not date_checker("2008-06-25T14:30:00.000000")
    assert not date_checker("2023-06-25T14:30:00.000000")

    with pytest.raises(ValueError):
        get_date_checker("invalid-date")
    with pytest.raises(ValueError):
        get_date_checker("2025-13-01")
