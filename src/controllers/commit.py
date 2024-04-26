from typing import Union
from config import get_value, get_subsection
from utils import execute_command
from version import change_version, get_version, get_version_by_file, replace_version
from rich import print

def main_branch() -> str:
    main = execute_command("git symbolic-ref refs/remotes/origin/HEAD")
    if 'fatal' in main:
        return 'main'
    return main.split('/')[-1].strip()


def difference_to_remote() -> str:
    main = main_branch()
    execute_command(f"git remote update")
    return execute_command(f"git diff {main} origin/{main}")

def check_new_commits() -> bool:
    """
    Check for new commits in all remote branches.
    """
    execute_command("git fetch")

    remote_branches = execute_command("git branch -r").split('\n')

    for branch in remote_branches:
        if '->' in branch:
            continue
        branch = branch.strip()
        new_commits = execute_command(f"git log HEAD..{branch} --oneline")

        if new_commits:
            print(f"La branche {branch} a de nouveaux commits :")
            print(new_commits)
            return True
    return False

def get_latest_commit() -> str:
    """
    Get latest commit.
    """
    latest_branch = execute_command("git for-each-ref --sort=-committerdate refs/remotes").split('\n')[0]

    return latest_branch.split(' ')[0]

def get_file_content(commit: str, file_path: str) -> str:
    """
    Get the content of a file at a specific commit.
    """
    file_content = execute_command(f"git show {commit}:{file_path}")

    return file_content


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

    # TODO check if the last commit is the same as the current one
    commit_hash = None

    if check_new_commits():
        commit_hash = get_latest_commit()
        print(commit_hash)

    for s in list(scope):
        try:
            files = get_subsection(f"scope.{s}.files")
        except Exception as e:
            continue # No files for this scope
        for f in files:
            path = get_value(f"scope.{s}.files.{f}.path")
            pattern = get_value(f"scope.{s}.files.{f}.pattern")
            try :
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
                    print(f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                    return
                new_version = change_version(old_version, version_type)
                replace_version(path, pattern, new_version)
                print("nv " + new_version)
            except Exception as e:
                print(f"[red]Error on changement of version for scope {s} and file {path}[/red]")
                print(repr(e))
                return
            execute_command(f"git add {path}")

    if type(scope)== list:
        scope = '|'.join(scope)
    message = ' | '.join(message)


    commit_message = f"{_type}({scope}): {message}".lower()
    print(commit_message)

    execute_command(f"git commit -m \"{commit_message}\"")
    execute_command(f"git push")