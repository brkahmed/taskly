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
    ...


def load_database() -> dict[str, dict]: ...


def save_database(database: dict[str, dict]) -> None: ...


def get_querie(supported_queries: dict[str, dict]) -> tuple[str, tuple]: ...


def add_task(database: dict[str, dict], description: str) -> None: ...


def delete_task(database: dict[str, dict], id: int) -> None: ...


def update_task(database: dict[str, dict], id: int, description: str) -> None: ...


def list_task(
    database: dict[str, dict],
    type: Literal["all", "done", "in-progress", "todo"] = "all",
) -> None: ...


def mark_in_progress_task(database: dict[str, dict], id: int) -> None: ...


def mark_done_task(database: dict[str, dict], id: int) -> None: ...


if __name__ == "__main__":
    main()
