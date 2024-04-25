from rich import print
from config import get_section, get_subsection, set_value, remove_section, get_value
from version import change_version, get_version, get_version_by_file, replace_version

from version import PATTERN, VERSION


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

def check(name: str) -> None:
    try:
        files = get_subsection(f"scope.{name}.files")
    except Exception as e:
        print(f"[red]No files to check for this scope.[/red]")
        return

    for f in files:
        path = get_value(f"scope.{name}.files.{f}.path")
        pattern = get_value(f"scope.{name}.files.{f}.pattern")
        print(f"[green]-- Checking {path} with pattern {pattern} --[/green]")
        try:
            old_version: str = get_version_by_file(path, pattern)
            print(f"[green]Find [bold]{old_version}[/bold] version[/green]")
            if old_version is None:
                print(f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                return
            new_version = change_version(old_version, VERSION.PATCH.value)
            print(f"[green]The new version is [bold]{new_version}[/bold][/green]")
        except Exception as e:
            print(f"[red]Error on pattern for {path} with pattern {pattern}[/red]")
            print(repr(e))

def remove(name: str) -> None:
    remove_section(f"scope.{name}")
    print(f"[green]The scope [bold]{name}[/bold] has been removed.[/green]")

def modify(name: str, property: str, value: str) -> None:
    set_value(f"scope.{name}.{property}", value)
    print(f"[green]The scope [bold]{name}[/bold] has been modified.[/green]")