"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import subprocess
from commands.base import BaseCommand, ROOT_COMMANDS

from __config__ import PATH

from env import default_env

class InitMakeCommand(BaseCommand):
    """
    Init command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'init'
    COMMAND_DESCRIPTION = 'Init gitbenchmark to the project'
    COMMAND_ARGS = [
        {"name": "existing", "help": "add gitbenchmark to existing project", "type": bool, "default": False,
         "message": "Add gitbenchmark to existing project ?"},

    ]
    COMMAND_FLAGS = [
        {"name": "--message", "action": "store_true", "help": "Increment the minor version", "type": str, "default": "chore: initial commit"},
        {"name": "--branch", "action": "store", "help": "Set the main branch"}
    ]

    def initialize_config(self):
        WORKSPACE = os.path.join(os.getcwd(), PATH)

        # create .env
        with open(os.path.join(WORKSPACE, '.env'), 'w') as f:
            f.write(default_env)

        default_gitignore = """# Gitbenchmark
.gitbenchmark/.env
.gitbenchmark/stacktrace.json
.gitbenchmark/app.log
"""

        # create .gitignore
        with open(os.path.join(os.getcwd(), '.gitignore'), 'w') as f:
            f.write(default_gitignore)

    def initialize_project(self, existing: bool, main_branch: str, release_branch: str):
        """
        Initialize the project with git
        """
        if not existing:
            subprocess.run(["git", "init"])
            subprocess.run(["git", "branch", "-M", main_branch])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "chore: initial gitbenchmark"])
        subprocess.run(["git", "branch", release_branch])

    def run(self, args):
        super().run(args)
        main_branch = "main"
        release_branch = "release"

        if args.branch:
            main_branch = args.branch

        if not args.existing:
            self.initialize_config()
        else : 
            # check if git is initialized
            if subprocess.run(["git", "status"]).returncode != 0:
                print("Git is not initialized, please choose existing value to False")
                return
        self.initialize_project(args.existing, main_branch, release_branch)

    def rollback(self):
        super().rollback()

    def register(self):
        super().register()