"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import subprocess
import inquirer

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
    COMMAND_FLAGS = [
        {"name": "--default", "action": "store_true", "help": "Use default values"},
    ]

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
                    pass

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

    @abstractmethod
    def run(self, args):
        """
        Run the command.
        """
        self.__setup_inquierer(args)
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
