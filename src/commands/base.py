"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""


import argparse

from __config__ import NAME, VERSION

from commands.manager import CommandManager

# create the top-level parser
parser = argparse.ArgumentParser(description=f"{NAME} {VERSION}")
parser.add_argument('-v', '--version', action='version', version=f"{NAME} {VERSION}")

# create subparsers
subparsers = parser.add_subparsers(dest='command')

# create the command manager
manager = CommandManager()

# add commands to the parser
for command_name, command_details in manager.commands.items():
    command_parser = subparsers.add_parser(command_name, help=f"{command_name} command")

    # add flags and args which are specified in the command class to the parser
    if "flags" in command_details:
        for flag in command_details["flags"]:
            command_parser.add_argument(flag["name"], action=flag["action"], help=flag["help"])

    if "args" in command_details:
        for arg in command_details["args"]:
            command_parser.add_argument(arg["name"], help=arg["help"])

# initialize the parser
args = parser.parse_args()

if args.command:
    manager.run_command(args.command, args)
else:
    parser.print_help()
