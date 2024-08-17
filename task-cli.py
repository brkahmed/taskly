from typing import Literal

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
                    'name_or_flags': []
                    'type': Callable,
                    'help': str,
                    'choices': []
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


def load_database() -> dict[str, dict]: ...


def save_database(database: dict[str, dict]) -> None: ...


def get_querie(supported_queries: dict[str, dict]) -> tuple[str, tuple]: ...


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
