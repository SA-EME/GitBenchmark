"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from commands.base import BaseCommand

class RollbackCommand(BaseCommand):
    """
    Rollback command class.
    """
    REQUIRED_CONFIG = False

    COMMAND_NAME = 'rollback'
    COMMAND_DESCRIPTION = 'rollback everything before last commit'
    COMMAND_ARGS = []
    COMMAND_FLAGS = []

    def run(self, args):
        super().run(args)
        print("Rollback")

    def rollback(self):
        pass

    def register(self):
        pass