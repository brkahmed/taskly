from typing import Literal, Callable
from argparse import ArgumentParser
import json

"""
database schema:
    {
        'id': {
            'description': str,
            'status': str,
            'created-at': str,
            'updated-at': str
        },
    }
supported queries schema:
    {
        'name': {
            'target': Callable,
            'help': str,
            'args': [
                {
                    'name_or_flags': ['str', ]
                    'type': Callable,
                    'help': str,
                    'choices': [Any, ],
                    'default': Any
                },
            ]
        },
    }
"""


def main() -> None:
    supported_queries = {
        "add": {
            "target": add_task,
            "help": "add task to your list",
            "args": [{"name_or_flags": ["description"], "help": "task description"}],
        },
        "delete": {
            "target": delete_task,
            "help": "delete task from your list",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "id of task you want to delete",
                    "type": int,
                }
            ],
        },
        "update": {
            "target": update_task,
            "help": "update task description",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "id of task you want to update",
                    "type": int,
                },
                {
                    "name_or_flags": ["description"],
                    "help": "new description for the task",
                },
            ],
        },
        "list": {
            "target": list_task,
            "help": "list all yout task",
            "args": [
                {
                    "name_or_flags": ["--status", "-s"],
                    "help": "status of task you want to list by default is all",
                    "choices": ["all", "done", "todo", "in-progress"],
                    "type": str.lower,
                    "default": "all",
                }
            ],
        },
        "mark-in-progress": {
            "target": mark_in_progress_task,
            "help": "set status of task to in-progress",
            "args": [{"name_or_flags": ["id"], "help": "id of task", "type": int}],
        },
        "mark-done": {
            "target": mark_done_task,
            "help": "set status of task to done",
            "args": [{"name_or_flags": ["id"], "help": "id of task", "type": int}],
        },
    }

    querie, args = get_querie(supported_queries)
    
    database: dict[str, dict] = load_database()

    querie(database, *args)

    save_database(database)

def load_database() -> dict[str, dict]:
    try:
        with open("task.json") as f:
            database = json.load(f)
    except FileNotFoundError:
        database = {}
    return database


def save_database(database: dict[str, dict]) -> None: ...


def get_querie(supported_queries: dict[str, dict]) -> tuple[Callable, dict]:
    parser: ArgumentParser = ArgumentParser(
        description="A cli app that makes manage tasks easy"
    )
    sub_parsers = parser.add_subparsers(title="commands", dest="command", required=True)

    for name, properties in supported_queries.items():
        p = sub_parsers.add_parser(name, help=properties["help"])
        for arg in properties["args"]:
            p.add_argument(*arg.pop("name_or_flags"), **arg)

    args: dict = parser.parse_args().__dict__
    querie: Callable = supported_queries[args.pop("command")]["target"]

    return querie, args


def add_task(database: dict[str, dict], description: str) -> None: ...


def delete_task(database: dict[str, dict], id: int) -> None: ...


def update_task(database: dict[str, dict], id: int, description: str) -> None: ...


def list_task(
    database: dict[str, dict],
    status: Literal["all", "done", "in-progress", "todo"] = "all",
) -> None: ...


def mark_in_progress_task(database: dict[str, dict], id: int) -> None: ...


def mark_done_task(database: dict[str, dict], id: int) -> None: ...


if __name__ == "__main__":
    main()
