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

class InitConfigCommand(BaseCommand):
    """
    Command class to initialize a new configuration file.
    """
    REQUIRED_CONFIG = False

    COMMAND_ROOT = ROOT_COMMANDS.config

    COMMAND_NAME = 'init'
    COMMAND_DESCRIPTION = 'create a new config file'
    COMMAND_ARGS = [
        {"name": "versioning", "help": "enable/disable version manager", "type": bool,
         "default": True, "message": "Use version manager ?"},
        {"name": "prerelease", "help": "enable/disable prerelease", "type": bool,
         "default": False, "message": "Use version manager ?"},
        {"name": "logging", "help": "enable/disable changelog manager", "type": bool,
         "default": True, "message": "Use changelog manager ?"},
        {"name": "commit", "help": "enable/disable conventional commit", "type": bool,
         "default": True, "message": "Use changelog manager ?"},
    ]
    COMMAND_FLAGS = [
        {"name": "--default", "action": "store_true", "help": "Use default values"},
        {"name": "--verbose", "action": "store_true", "help": "Active verbose"}
    ]


    def run(self, args):
        super().run(args)
        if args.verbose:
            print("Running init command with args")
            print(args.versioning)
            print(args.logging)

        WORKSPACE = os.path.join(os.getcwd(), PATH)

        if not os.path.exists(os.path.join(os.getcwd(), PATH)):
            os.makedirs(os.path.join(os.getcwd(), PATH))

        config_content = default_config.format(
            versioning=args.versioning,
            prerelease=args.prerelease,
            logging=args.logging,
            commit=args.commit,
            version='{version}'
        )

        with open(os.path.join(WORKSPACE, 'config.toml'), 'w', encoding='utf8') as f:
            f.write(config_content)

    def register(self):
        pass

    def rollback(self):
        pass
