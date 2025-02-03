"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os

from commands.base import BaseCommand, ROOT_COMMANDS

from __config__ import PATH

from config.schemas import default_config

class ChangelogConfigCommand(BaseCommand):
    """
    Command class to initialize a new configuration file.
    """

    COMMAND_ROOT = ROOT_COMMANDS.config

    COMMAND_NAME = 'changelog'
    COMMAND_DESCRIPTION = 'create a new config file'
    COMMAND_ARGS = [
        {"name": "versioning", "help": "enable/disable version manager", "type": bool, "default": True,
         "message": "Use version manager ?"},
        {"name": "logging", "help": "enable/disable changelog manager", "type": bool, "default": True,
         "message": "Use changelog manager ?"},
        {"name": "commit", "help": "enable/disable conventional commit", "type": bool, "default": True,
         "message": "Use changelog manager ?"},
        {"name": "message", "help": "Message of commit", "type": str, "default": "chore: initial commit", "message": "Quel messages ?",}
    ]
    COMMAND_FLAGS = [
        {"name": "--verbose", "action": "store_true", "help": "Active verbose"}
    ]


    def run(self, args):
        super().run(args)
        if args.verbose:
            print("Running init command with args")
            print(args.versioning)
            print(args.logging)
            print(args.message)

        WORKSPACE = os.path.join(os.getcwd(), PATH)

        if not os.path.exists(os.path.join(os.getcwd(), PATH)):
           os.makedirs(os.path.join(os.getcwd(), PATH))

        config_content = default_config.format(
            versioning=args.versioning,
            logging=args.logging,
            commit=args.commit,
            message=args.message
        )


        with open(os.path.join(WORKSPACE, 'config.toml'), 'w') as f:
            f.write(config_content)

    def register(self):
        pass

    def rollback(self):
        pass
