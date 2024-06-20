from rich import print
from types import SimpleNamespace

from utils.git import main_branch
from utils.process import execute_command

from arguments.commit import commit_arguments


def merge(merged_branch: str = None):
    if not merged_branch:
        return

    commit_arguments(args=SimpleNamespace(command='merge', params=[]))

    execute_command(f"git checkout {main_branch()}")
    execute_command(f"git merge --squash {merged_branch}")

    print(f"[green]Branch {merged_branch} merged in {main_branch()}[/green]")

    execute_command("git commit")
    execute_command(f"git push")
    execute_command(f"git branch -d {merged_branch}")
