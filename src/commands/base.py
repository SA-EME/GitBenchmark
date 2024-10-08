"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from stacktrace import stacktrace_manager

@dataclass
class CommandName:
    """
    Every command root name.
    """
    make: str = "make"
    config: str = "config"


ROOT_COMMANDS = CommandName()


class BaseCommand(ABC):
    """
    Next command class.
    """

    COMMAND_ROOT = None

    COMMAND_NAME = ''
    COMMAND_DESCRIPTION = ''
    COMMAND_ARGS = []
    COMMAND_FLAGS = []

    @abstractmethod
    def run(self, args):
        """
        Run the command.
        """
        self.register()

    @abstractmethod
    def register(self):
        """
        Register the command.
        """
        stacktrace_manager.register_action(self.full_name(), 'registered', None)


    @abstractmethod
    def rollback(self):
        """
        Rollback the command.
        """

    def full_name(self) -> str:
        """
        Get the full name of the command.
        """
        return f"{self.COMMAND_ROOT}:{self.COMMAND_NAME}"
