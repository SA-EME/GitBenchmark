from rich import print
from typing import Union
from config import get_value, get_subsection
from utils.process import execute_command
from version import change_version, get_version_by_file, replace_version, VERSION


def build(scope):
    version_type = VERSION.BUILD.value

    # TODO : Duplicate code, refactor
    try:
        files = get_subsection(f"scope.{scope}.files")
    except Exception as e:
        print(f"[red]No files to check for this scope {scope}[/red]")
        return 0
    for f in files:
        path = get_value(f"scope.{scope}.files.{f}.path")
        pattern = get_value(f"scope.{scope}.files.{f}.pattern")
        try:
            old_version: str = get_version_by_file(path, pattern)
            print("ov " + old_version)
            if old_version is None:
                print(f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                return 0
            new_version = change_version(old_version, version_type)
            replace_version(path, pattern, new_version)
            print("nv " + new_version)
        except Exception as e:
            print(f"[red]Error on changement of version for scope {scope} and file {path}[/red]")
            print(repr(e))
            return 0
    return 1
