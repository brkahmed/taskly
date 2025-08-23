import json
import operator
import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from inspect import signature
from typing import (
    Annotated,
    Callable,
    Literal,
    Optional,
    TypeAlias,
    TypedDict,
    Union,
    get_args,
    get_origin,
)

from tabulate import tabulate

supported_queries: dict[str, dict] = {}
TaskStatus: TypeAlias = Literal["done", "in-progress", "todo"]
DatabaseRow = TypedDict(
    "DatabaseRow",
    {"description": str, "status": TaskStatus, "created-at": str, "updated-at": str},
)
Database: TypeAlias = dict[str, DatabaseRow]


def main() -> None:
    query, args = parse_args()

    DATABASE_PATH: str = os.path.expanduser("~/taskly.json")

    database: Database = load_database(DATABASE_PATH)

    try:
        query(database, **args)
    except Exception as e:
        sys.exit(str(e))

    save_database(database, DATABASE_PATH)


def load_database(path: str) -> Database:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_database(database: Database, path: str) -> None:
    with open(path, "w") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)


def parse_args() -> tuple[Callable, dict]:
    parser: ArgumentParser = ArgumentParser(description="A CLI application to efficiently manage your tasks")
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)

    for name, properties in supported_queries.items():
        p = subparsers.add_parser(name, help=properties["help"])
        for arg in properties["args"]:
            name_or_flags = arg.pop("name_or_flags")
            p.add_argument(*name_or_flags, **arg)
            arg["name_or_flags"] = name_or_flags  # to keep the original name or flags

    args: dict = vars(parser.parse_args())
    query: Callable = supported_queries[args.pop("command")]["target"]

    return query, args


def add_query(func: Callable) -> Callable:
    """Decorator to add a query to the supported queries dictionary."""
    name = func.__name__.removesuffix("_task").replace("_", "-")
    supported_queries[name] = {
        "target": func,
        "help": func.__doc__,
        "args": [],
    }
    args = supported_queries[name]["args"]
    for param in signature(func).parameters.values():
        if param.name == "database":
            continue
        type, *metadata = get_args(param.annotation)
        if get_origin(type) is Union:
            type = get_args(type)[0]
        args.append(
            {
                "name_or_flags": metadata[1:] if len(metadata) > 1 else [param.name],
                "help": metadata[0],
                "choices": get_args(type) if get_origin(type) is Literal else None,
                "default": param.default if param.default is not param.empty else None,
            }
        )
    return func


@add_query
def add_task(
    database: Database,
    description: Annotated[str, "Description of the task"],
) -> None:
    """Add a new task to your task list"""
    today: str = datetime.today().isoformat(timespec="seconds")
    id: str = str(max(map(int, database.keys()), default=0) + 1)
    database[id] = {
        "description": description,
        "status": "todo",
        "created-at": today,
        "updated-at": today,
    }
    list_task({id: database[id]})


@add_query
def update_task(
    database: Database,
    id: Annotated[str, "ID of the task you want to update"],
    description: Annotated[Optional[str], "New description for the task", "--description", "-d"] = None,
    status: Annotated[Optional[TaskStatus], "New status for the task", "--status", "-s"] = None,
) -> None:
    """Update the description or status of a task"""
    if id not in database:
        raise KeyError(f"No task found with ID '{id}'")
    if description is not None:
        database[id]["description"] = description
    if status is not None:
        if status not in (valid := get_args(TaskStatus)):
            raise ValueError(f"Invalid status '{status}'. Valid statuses are: {', '.join(valid)}")
        database[id]["status"] = status
    database[id]["updated-at"] = datetime.today().isoformat(timespec="seconds")
    list_task({id: database[id]})


@add_query
def mark_in_progress_task(
    database: Database,
    id: Annotated[str, "ID of the task"],
) -> None:
    """Mark a task as 'in-progress'"""
    update_task(database, id, status="in-progress")


@add_query
def mark_done_task(
    database: Database,
    id: Annotated[str, "ID of the task"],
) -> None:
    """Mark a task as 'done'"""
    update_task(database, id, status="done")


@add_query
def delete_task(
    database: Database,
    id: Annotated[str, "ID of the task you want to delete"],
) -> None:
    """Delete a task from your task list"""
    if id not in database:
        raise KeyError(f"No task found with ID '{id}'")
    list_task({id: database[id]})
    del database[id]


@add_query
def list_task(
    database: Database,
    status: Annotated[Literal[TaskStatus, "all"], "List all tasks or filter them by status", "--status", "-s"] = "all",
    date: Annotated[
        Optional[str],
        "Filter tasks by date (YYYY-MM-DD). Use <, >, = operators (e.g. '<2025-01-01' means on or before)",
        "--date",
        "-d",
    ] = None,
) -> None:
    """List all tasks or filter them by status and date"""
    DATETIME_FORMAT: str = "%Y/%m/%d %H:%M:%S"
    if status not in (valid := get_args(TaskStatus)) + ("all",):
        raise ValueError(f"Invalid status '{status}'. Valid statuses are: {', '.join(valid)} or 'all'")
    date_checker = get_date_checker(date)
    table = (
        {
            "Id": id,
            "Description": properties["description"],
            "Status": properties["status"],
            "Created At": datetime.fromisoformat(properties["created-at"]).strftime(DATETIME_FORMAT),
            "Updated At": datetime.fromisoformat(properties["updated-at"]).strftime(DATETIME_FORMAT),
        }
        for id, properties in sorted(database.items(), key=lambda t: t[0])
        if (status == "all" or status == properties["status"]) and date_checker(properties["created-at"])
    )
    print(tabulate(table, tablefmt="rounded_grid", headers="keys") or "Nothing to display")


def get_date_checker(date_string: Optional[str] = None) -> Callable[[str], bool]:
    if date_string is None:
        return lambda _: True  # If no date is provided, return True for all dates
    operators = {
        "<": operator.le,
        ">": operator.ge,
        "=": operator.eq,
    }  # mapping < to le is not a bug, it is intentional
    op = "="  # this line is not needed i just add it to ignore unbound warning
    for op in operators.keys():  # default to '='
        if date_string.startswith(op):
            date_string = date_string[len(op) :].strip()
            break

    for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
        try:
            date = datetime.strptime(date_string, fmt).date()
            return lambda other: operators[op](datetime.strptime(other[: len(date_string)], fmt).date(), date)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: '{date_string}'. Expected formats: YYYY-MM-DD, YYYY-MM, or YYYY.")


if __name__ == "__main__":
    main()
