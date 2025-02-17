"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import logging
from commands.base import BaseCommand, ROOT_COMMANDS

from stacktrace import stacktrace_manager



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
        for action in stacktrace_manager.get_all_actions():
            if "command" in action:
                if ':' in action["command"]:
                    command = stacktrace_manager.get_rollback_command(action["command"])
                    command.rollback(action["content"])
                    continue
            logging.warning("Detected stacktrace without command")


    def register(self):
        super().register()

    def rollback(self):
        """
        remove rollback system for the rollback command
        """
        pass