from rich import print
from version import VERSION
from config import get_section, set_value, remove_section, get_value



def show() -> None:
    """List all scopes or types."""
    for scope in get_section('type'):
        print(f"[green]{scope}[/green]")

def exist(type: str) -> bool:
    """Check if a type exists."""
    if type in get_section('type'):
        return True
    return False

def get(name: str) -> str:
    """Get a type by name."""
    return get_value(f"scope.{name}")

def add(name: str, version: str) -> None:
    if (exist(name)):
        print(f"[yellow]This type [bold]{name}[/bold] already exists.[/yellow]")
        return

    set_value(f"type.{name}.version", version)
    print(f"[green]The type [bold]{name}[/bold] has been added.[/green]")

def remove(name: str) -> None:
    if not exist(name):
        print(f"[yellow]This type [bold]{name}[/bold] don't exists.[/yellow]")
        return

    remove_section(f"type.{name}")
    print(f"[green]The type [bold]{name}[/bold] has been removed.[/green]")
