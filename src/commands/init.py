"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import subprocess
import logging
from commands.base import BaseCommand

from __config__ import PATH

from env import DEFAULT_ENV
from config.schemas import default_config

from stacktrace import stacktrace_manager

class InitCommand(BaseCommand):
    """
    Init command class.
    """
    REQUIRED_CONFIG = False

    WORKSPACE = os.path.join(os.getcwd(), PATH)

    COMMAND_NAME = 'init'
    COMMAND_DESCRIPTION = 'init gitbenchmark to the project'
    COMMAND_ARGS = [
        {"name": "versioning", "help": "enable/disable version manager", "type": bool,
         "default": True, "message": "Use version manager ?"},
        {"name": "prerelease", "help": "enable/disable prerelease", "type": bool,
         "default": False, "message": "Use prerelease ?"},
        {"name": "logging", "help": "enable/disable changelog manager", "type": bool,
         "default": True, "message": "Use changelog manager ?"},
        {"name": "config_commit", "help": "enable/disable conventional commit", "type": bool,
         "default": True, "message": "Use changelog conventional commit ?"},
        {"name": "existing", "help": "add gitbenchmark to existing project", "type": bool,
         "default": False, "message": "Add gitbenchmark to existing project ?"},
    ]

    COMMAND_FLAGS = [
        {"name": "--commit", "action": "store_true", "help": "create a commit of the gitbenchmark init"},
    ]


    def initialize_config(self):

        # create .env
        with open(os.path.join(self.WORKSPACE, '.env'), 'w') as f:
            f.write(DEFAULT_ENV)

        default_gitignore = """# Gitbenchmark

.gitbenchmark/.env
.gitbenchmark/stacktrace.json
.gitbenchmark/app.log
.gitbenchmark/plugins
"""

        # create .gitignore
        with open(os.path.join(os.getcwd(), '.gitignore'), 'w', encoding='utf8') as f:
            f.write(default_gitignore)

    def initialize_project(self, existing: bool, commit: bool, main_branch: str, release_branch: str):
        """
        Initialize the project with git
        """
        if not existing:
            subprocess.run(["git", "init"])
            subprocess.run(["git", "branch", "-M", main_branch])
        if commit:
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "chore: initial gitbenchmark"])
            subprocess.run(["git", "branch", release_branch])

    def create_config(self, args):

        config_content = default_config.format(
            versioning=args.versioning,
            prerelease=args.prerelease,
            logging=args.logging,
            commit=args.config_commit,
            version='{version}'
        )

        with open(os.path.join(self.WORKSPACE, 'config.toml'), 'w', encoding='utf8') as f:
            f.write(config_content)

    def run(self, args):
        if os.path.exists(os.path.join(os.getcwd(), PATH)):
            logging.error(".gitbenchmark already init")
            return

        super().run(args)
        os.makedirs(os.path.join(os.getcwd(), PATH))
        main_branch = "main"
        release_branch = "release"

        if "branch" in args:
            main_branch = args.branch



 

        if not args.existing:
            self.initialize_config()
        else:
            # check if git is initialized
            if subprocess.run(["git", "status"]).returncode != 0:
                logging.warning("Git is not initialized, please choose existing value to False")
                return
        self.create_config(args)
        self.initialize_project(args.existing, args.commit, main_branch, release_branch)

        config = [
            {
                "existing_project": args.existing,
                "has_commit": args.commit
            }
        ]

        stacktrace_manager.register_action(self.references(), 'registered', config)


    def register(self):
        pass

    def rollback(self, content: any):
        config = content[0]
        subprocess.run(["rm", "-rf", ".gitbenchmark"])
        if not config["existing_project"]:
            subprocess.run(["rm", "-rf", ".git"])
        else :
            if config["has_commit"]:
                self.execute_command("git reset --soft HEAD~1")
