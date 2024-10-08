"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


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

    @abstractmethod
    def rollback(self):
        """
        Rollback the command.
        """
