"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from commands.base import BaseCommand, ROOT_COMMANDS


class ReleaseCommand(BaseCommand):
    """
    Release command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'release'
    COMMAND_DESCRIPTION = 'Release a new version of the project'
    COMMAND_ARGS = [
        {"name": "version", "help": "The version to release"}
    ]
    COMMAND_FLAGS = [
        {"name": "--minor", "action": "store_true", "help": "Increment the minor version"},
        {"name": "--major", "action": "store_true", "help": "Increment the major version"}
    ]

    def run(self, args):
        print(f"Running release command with args: {args}")
        if 'version' in args:
            version = args.version
            if (version is None):
                return

    def rollback(self):
        print("Rolling back the release...")

    def register(self):
        print("Registering release command...")
