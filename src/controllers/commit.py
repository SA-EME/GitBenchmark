from rich import print
from typing import Union
from config import get_value, get_subsection
from utils.process import execute_command
from version import change_version, get_version, get_version_by_file, replace_version

from utils.git import check_new_commits, get_latest_commit, get_current_branch, main_branch, push

# TODO : Remove this function if not used


def get_file_content(commit: str, file_path: str) -> str:
    """
    Get the content of a file at a specific commit.
    """
    file_content = execute_command(f"git show {commit}:{file_path}")

    return file_content

#  TODO : move this function to the version.py file


def versioning(_type, scope) -> bool:
    version_type = get_value(f"type.{_type}.version")

    # TODO : Duplicate code, refactor
    # TODO check if the last commit is the same as the current one
    commit_hash = None

    if check_new_commits():
        commit_hash = get_latest_commit()
        print(commit_hash)

    for s in list(scope):
        try:
            files = get_subsection(f"scope.{s}.files")
        except Exception as e:
            print("continue")
            continue  # No files for this scope
        for f in files:
            path = get_value(f"scope.{s}.files.{f}.path")
            pattern = get_value(f"scope.{s}.files.{f}.pattern")
            try:
                if commit_hash:
                    commit_content = get_file_content(commit_hash, path)
                    if commit_content:
                        print('[yellow]get version from last commit[/yellow]')
                        old_version: str = get_version(commit_content, pattern)
                    else:
                        old_version: str = get_version_by_file(path, pattern)
                else:
                    old_version: str = get_version_by_file(path, pattern)
                print("ov " + old_version)
                if old_version is None:
                    print(
                        f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                    return 0
                new_version = change_version(old_version, version_type)
                replace_version(path, pattern, new_version)
                print("nv " + new_version)
            except Exception as e:
                print(
                    f"[red]Error on changement of version for scope {s} and file {path}[/red]")
                print(repr(e))
                return 0
            execute_command(f"git add {path}")
        return 1


def commit(_command, _type, scope, message) -> Union[dict, None]:

    if get_current_branch() == main_branch():
        print("[yellow]Warning you are on the main branch, the commit will change the current version[/yellow]")
        print("[yellow]Do you want to continue?[/yellow]")
        continue_commit = input("Continue ? (y/n)")
        if continue_commit.lower() != 'y':
            return None

        if versioning(_type, scope) == 0:
            return None
    elif _command == 'merge':
        if versioning(_type, scope) == 0:
            return None

    if type(scope) == list:
        scope = '|'.join(scope)
    message = ' | '.join(message)

    commit_message = f"{_type}({scope}): {message}".lower()
    print(commit_message)

    execute_command(f"git commit -m \"{commit_message}\"")
    push()
