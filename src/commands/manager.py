"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import logging

from commands.base import ROOT_COMMANDS

from commands.plugin import load_plugins


class CommandManager:
    """"
    Command manager class that handles the default commands and plugins commands.
    """
    def __init__(self):
        self.commands = []
        self.load_commands()

        # Load plugins
        self.plugins = load_plugins()
        for plugin in self.plugins.values():
            self.commands.extend(plugin.register_commands())

    def load_commands(self):
        """
        Dynamically load all orders and save them in the system.
        """
        command_classes = [
            ("commands.make.init", "InitMakeCommand"),
            ("commands.config.init", "InitConfigCommand"),
            ("commands.make.commit", "CommitMakeCommand"),
            ("commands.config.changelog", "ChangelogConfigCommand"),
            ("commands.make.changelog", "ChangelogCommand"),
            ("commands.make.release", "ReleaseCommand"),
        ]

        for module_name, class_name in command_classes:
            try:
                module = __import__(module_name, fromlist=[class_name])
                command_class = getattr(module, class_name)

                instance = command_class()

                self.load_command(instance)
            except Exception as e:
                logging.warning(f"⚠️ Skipping {class_name}: {e}")


    def load_command(self, command_class):
        """
        Load an order and save it in the system.
        """
        # command_instance = command_class()
        self.commands.append(command_class)

    def add_commands_to_parser(self, subparsers):
        """
        Add loaded commands to argument parser.
        """
        root_parsers = {}
        for command in self.commands:
            if hasattr(command, 'COMMAND_ROOT') and command.COMMAND_ROOT in ROOT_COMMANDS.__dict__.values():
                if command.COMMAND_ROOT not in root_parsers:
                    root_parsers[command.COMMAND_ROOT] = subparsers.add_parser(
                        command.COMMAND_ROOT, help=f"{command.COMMAND_ROOT} related commands"
                    ).add_subparsers(dest=f"{command.COMMAND_ROOT}_subcommand")
                self.add_subcommands(root_parsers[command.COMMAND_ROOT], command)
            else:
                self.add_subcommands(subparsers, command)

    def add_subcommands(self, subparsers, command):
        """
        Adding sub-commands linked to a prefix.
        """
        subparser = subparsers.add_parser(command.COMMAND_NAME, help=command.COMMAND_DESCRIPTION)
        for arg in command.COMMAND_ARGS:
            subparser.add_argument(arg["name"], help=arg["help"], nargs='?', default=None)
        for flag in command.COMMAND_FLAGS:
            subparser.add_argument(flag["name"], action=flag["action"], help=flag["help"])
        subparser.set_defaults(func=command.run)

    def run_command(self, root_command, subcommand_name, args):
        """
        Run the command with the given root command and subcommand name.
        Args:
            root_command (str): The root command (e.g., 'make', 'config').
            subcommand_name (str): The name of the subcommand to run.
            args (Namespace): The arguments passed to the command.
        """
        for command in self.commands:
            if command.COMMAND_ROOT == root_command and command.COMMAND_NAME == subcommand_name:
                command.run(args)
                return
        logging.warning("Unknown subcommand: %s %s", root_command, subcommand_name)
