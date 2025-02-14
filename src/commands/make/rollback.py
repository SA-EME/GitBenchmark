"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from commands.base import BaseCommand, ROOT_COMMANDS


class RollbackMakeCommand(BaseCommand):
    """
    Release command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'rollback'
    COMMAND_DESCRIPTION = 'rollback everything before last commit'
    COMMAND_ARGS = []
    COMMAND_FLAGS = []

    def run(self, args):
        super().run(args)
        print("Rollback")

    def register(self):
        super().register()

    def rollback(self):
        """
        remove rollback system for the rollback command
        """
        pass