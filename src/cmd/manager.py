"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import logging
import importlib
import commands

from cmd.base import ROOT_COMMANDS

from plugin import load_plugins


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
        Dynamically load all commands and save them in the system.
        """
        for module_name in commands.__all__:
            try:
                module = importlib.import_module(module_name)
                command_name = module_name.split(".")[-1].capitalize()
                command_sub_name = module_name.split(".")[-2].capitalize() if len(module_name.split(".")) > 2 else ""
                class_name = command_name + command_sub_name  + "Command"

                if hasattr(module, class_name):
                    command_class = getattr(module, class_name)
                    instance = command_class()

                    if (instance.REQUIRED_CONFIG and not os.path.exists(os.path.join('.gitbenchmark', '.env'))):
                        continue
                    self.load_command(instance)
            except Exception as e:
                logging.warning("⚠️ Skipping %s: %s", class_name, e)


    def load_command(self, command_class):
        """
        Load an order and save it in the system.
        """
        self.commands.append(command_class)

    def add_commands_to_parser(self, subparsers):
        """
        Add loaded commands to argument parser.
        """
        root_parsers = {}
        for command in self.commands:
            if (hasattr(command, 'COMMAND_ROOT') 
                and command.COMMAND_ROOT in ROOT_COMMANDS.__dict__.values()):
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
        for flag in command.get_command_flags():
            subparser.add_argument(flag["name"], action=flag["action"], help=flag["help"])
        subparser.set_defaults(func=command.run)

    def run_subcommand(self, root_command, subcommand_name, args):
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

    def run_command(self, root_command, args):
        """
        Run the command with the given root command and subcommand name.
        Args:
            command (str): The root command (e.g., 'make', 'config').
            args (Namespace): The arguments passed to the command.
        """
        for command in self.commands:
            if command.COMMAND_NAME == root_command:
                command.run(args)
                return
        logging.warning("Unknown subcommand: %s", root_command)
