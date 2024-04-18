from rich import print
from config import get_section, set_value, remove_section, get_value

from version import PATTERN


def show() -> None:
    """List all scopes or types."""
    for scope in get_section('scope'):
        print(f"[green]{scope}[/green]")

def exist(scope: str) -> bool:
    """Check if a scope or type exists."""
    if scope in get_section('scope'):
        return True
    return False

def get(name: str) -> str:
    """Get a scope or type by name."""
    return get_value(f"scope.{name}")

def add(name: str, main: str, pattern: PATTERN) -> None:
    set_value(f"scope.{name}.files.main.path", main)
    set_value(f"scope.{name}.files.main.pattern", pattern)
    print(f"[green]The scope [bold]{name}[/bold] has been added.[/green]")

def remove(name: str) -> None:
    remove_section(f"scope.{name}")
    print(f"[green]The scope [bold]{name}[/bold] has been removed.[/green]")

def modify(name: str, property: str, value: str) -> None:
    set_value(f"scope.{name}.{property}", value)
    print(f"[green]The scope [bold]{name}[/bold] has been modified.[/green]")