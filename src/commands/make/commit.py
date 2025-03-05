"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.

"""

from cmd.base import BaseCommand, ROOT_COMMANDS


class CommitMakeCommand(BaseCommand):
    """
    Init command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'commit'
    COMMAND_DESCRIPTION = 'commit the of the project'

    COMMAND_FLAGS = [
    ]

    def __init__(self):
        super().__init__()
        self.COMMAND_ARGS = [
        {
            "name": "type",
            "help": "Type of commit",
            "type": list,
            "default": "chore: initial commit",
            "message": "Quel type de commit voulez-vous effectuer ?",
            "choices": self.config.ConventionalCommits.type
        },
        {
            "name": "scope",
            "help": "Scope of commit",
            "type": list, 
            "default": "chore: initial commit",
            "message": "Quel scope ?",
            "choices": ['frontend', 'backend'],
            "optional": not self.config.Scope.enabled
        },
        {
            "name": "message",
            "help": "Message of commit",
            "type": str,
            "default": "chore: initial commit",
            "message": "Quel messages ?"
         }
    ]

    def commit(self, args):
        if args.scope:
            commit_message = f"{args.type}({args.scope}): {args.message.lower()}"
        else:
            commit_message = f"{args.type}: {args.message.lower()}"
        self.execute_command("git add .")
        self.execute_command(f"git commit -m \"{commit_message}\"")

    def run(self, args):
        super().run(args)
        self.commit(args)

    def register(self):
        pass # No need to register this command

    def rollback(self):
        super().rollback()
        self.execute_command("git reset --soft HEAD~1")

