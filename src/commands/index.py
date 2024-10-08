"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""


import argparse
from commands.manager import CommandManager

from __config__ import NAME, VERSION

# create the top-level parser
parser = argparse.ArgumentParser(description=f"{NAME} {VERSION}")
parser.add_argument('-v', '--version', action='version', version=f"{NAME} {VERSION}")

# create subparsers
subparsers = parser.add_subparsers(dest='root_command')

# create the command manager
manager = CommandManager()

# add commands to the parser
manager.add_commands_to_parser(subparsers)

# initialize the parser
args = parser.parse_args()

if args.root_command:
    subcommand_attr = f"{args.root_command}_subcommand"
    if hasattr(args, subcommand_attr):
        subcommand = getattr(args, subcommand_attr)
        if subcommand:
            manager.run_command(args.root_command, subcommand, args)
        else:
            parser.print_help()
    else:
        parser.print_help()
else:
    parser.print_help()
