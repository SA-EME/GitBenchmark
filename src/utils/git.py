from rich import print

from utils.process import execute_command
import inquirer

def main_branch() -> str:
    main = execute_command("git symbolic-ref refs/remotes/origin/HEAD")
    if 'fatal' in main:
        return 'main'
    return main.split('/')[-1].strip()

def get_current_branch() -> str:
    current = execute_command("git branch --show-current")
    return current

def difference_to_remote() -> str:
    main = main_branch()
    execute_command(f"git remote update")
    return execute_command(f"git diff {main} origin/{main}")

def push() -> str:
    message = execute_command("git push")
    if 'fatal' in message:
        remote_branch = inquirer.prompt([inquirer.Text('branch', message=f"How do you want to name the remote branch?")])["branch"]
        message = execute_command(f"git push --set-upstream origin {remote_branch}")
        print(message)

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


def check_commit() -> bool:
    output = execute_command("git diff --cached ")
    if not output:
        print("[red]There are no changes to commit, maybe add a file to commit[/red]")
        return False

    # TODO : Remove this if not used
    # if difference_to_remote():
    #     print("[red]You have to pull or push the changes before commiting[/red]")
    #     return False
    return True