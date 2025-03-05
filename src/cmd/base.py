"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import sys
import os
import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass

import subprocess
import inquirer

from config.index import config, Config
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
    REQUIRED_CONFIG = True


    COMMAND_ROOT = None

    COMMAND_NAME = ''
    COMMAND_DESCRIPTION = ''
    COMMAND_ARGS = []
    COMMAND_FLAGS = []

    # default commands flags
    __COMMAND_FLAGS = [
        {"name": "--default", "action": "store_true", "help": "Use default values"},
        {"name": "--verbos", "action": "store_true", "help": "Active verbose"} # TODO need to implement with log system
    ]

    config: None|Config = None

    def __setup_inquierer(self, args):
        """
        Setup inquirer for command.
        """
        for arg in self.COMMAND_ARGS:
            arg_name = arg["name"]

            # if default flag is present, skip inquirer
            if 'default' in args:
                if args.default:
                    setattr(args, arg_name, arg.get("default"))

            # Check if argument is missing
            if not hasattr(args, arg_name) or getattr(args, arg_name) is None:
                if "optional" in arg:
                    if arg["optional"] is True:
                        continue
                # Use inquirer if choices are defined in COMMAND_ARGS
                if "type" in arg :#if "choices" in arg and "message" in arg:
                    if arg["type"] is list:
                        questions = [
                            inquirer.List(arg_name,
                                        message=arg["message"],
                                        choices=arg["choices"])
                        ]
                        answers = inquirer.prompt(questions)
                        setattr(args, arg_name, answers[arg_name])
                    elif arg["type"] is str:
                        questions = [
                            inquirer.Text(arg_name,
                                        message=arg["message"])
                        ]
                        answers = inquirer.prompt(questions)
                        setattr(args, arg_name, answers[arg_name])
                    elif arg["type"] is bool:
                        questions = [
                            inquirer.Confirm(arg_name,
                                        message=arg["message"])
                        ]
                        answers = inquirer.prompt(questions)
                        setattr(args, arg_name, answers[arg_name])
                    else:
                        print("Type not supported")
                else:
                    # Use default if present
                    setattr(args, arg_name, arg.get("default"))

    def execute_command(self, command):
        """
        Execute a command.
        """
        return subprocess.run(command, shell=True, check=True)

    def __init__(self):
        if self.REQUIRED_CONFIG:
            self.config: Config = config

    @abstractmethod
    def run(self, args):
        """
        Run the command.
        """
        self.__setup_inquierer(args)
        self.register()

    def get_command_flags(self):
        return self.__COMMAND_FLAGS + self.COMMAND_FLAGS

    @abstractmethod
    def register(self):
        """
        Register the command.
        """
        stacktrace_manager.register_action(self.references(), 'registered', None)


    @abstractmethod
    def rollback(self):
        """
        Rollback the command.
        """

    def full_name(self) -> str:
        """
        Get the full name of the command.
        """
        return f"{self.COMMAND_ROOT}:{self.COMMAND_NAME}".replace('None', 'main'), # Replace command without subcommand by main command

    def references(self) -> str:
        """
        Get the reference of the command
        """
        child_class_file = inspect.getfile(self.__class__)
        main_file_path = os.path.abspath(sys.modules['__main__'].__file__)
        main_dir = os.path.dirname(main_file_path)
        file = os.path.relpath(child_class_file, start=main_dir)
        return f"{file}:{self.__class__.__name__}"
