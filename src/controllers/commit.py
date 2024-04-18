from typing import Union
from config import get_value, get_subsection
from utils import execute_command
from version import change_version, get_version, replace_version
from rich import print

def main_branch() -> str:
    main = execute_command("git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'")
    if main:
        return main
    return 'main'


def difference_to_remote() -> str:
    main = main_branch()
    execute_command(f"git remote update")
    return execute_command(f"git diff {main} origin/{main}")


def check_commit() -> bool:
    output = execute_command("git diff --cached ")
    if not output:
        print("[red]There are no changes to commit, maybe add a file to commit[/red]")
        return False

    if difference_to_remote():
        print("[red]You have to pull or push the changes before commiting[/red]")
        return False
    return True

def commit(_type, scope, message) -> Union[dict,None]:

    version_type = get_value(f"type.{_type}.version")

    for s in list(scope):
        print(s)
        files = get_subsection(f"scope.{s}.files")
        print("test")
        for f in files:
            path = get_value(f"scope.{s}.files.{f}.path")
            pattern = get_value(f"scope.{s}.files.{f}.pattern")
            try :
                old_version: str = get_version(path, pattern)
                print("ov " + old_version)
                if old_version is None:
                    print(f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                    return
                new_version = change_version(old_version, version_type)
                replace_version(path, pattern, new_version)
                print("nv " + new_version)
            except Exception as e:
                print(f"[red]Error on the regex[/red]")
                print(e)
            execute_command(f"git add {path}")
        
    if type(scope)== list:
        scope = '|'.join(scope)
    message = ' | '.join(message)


    commit_message = f"{_type}({scope}): {message}"
    print(commit_message)

    execute_command(f"git commit -m '{commit_message}'")