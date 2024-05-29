import argparse


from arguments.init import init_arguments
from arguments.build import build_arguments

from arguments.scope import scope_arguments
from arguments.commit import commit_arguments
from arguments.type import type_arguments


COMMAND_WITHOUT_CONFIG = ['init', '--version']


parser = argparse.ArgumentParser(
    description="A command-line tool to help you to have compliance with your commit & easy the versioning.")
subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

parser_init = subparsers.add_parser('init', help='Init gitbenchmark')
parser_init.set_defaults(func=init_arguments)

parser_build = subparsers.add_parser('build', help='Build help')
parser_build.add_argument('params', nargs='*', default=None, help='The scope to add or remove')
parser_build.set_defaults(func=build_arguments)

parser_scope = subparsers.add_parser('scope', help='Config scope help')
parser_scope.add_argument('action', choices=[
                          'add', 'remove', 'list', 'check'], help='The action to perform on the scope')
parser_scope.add_argument(
    'params', nargs='*', default=None, help='The scope to add or remove')
parser_scope.set_defaults(func=scope_arguments)

parser_type = subparsers.add_parser('type', help='Config type help')
parser_type.add_argument('action', choices=[
                         'add', 'remove', 'list'], help='The action to perform on the type')
parser_type.add_argument('params', nargs='*', default=None,
                         help='The type to add or remove')
parser_type.set_defaults(func=type_arguments)

parser_commit = subparsers.add_parser('commit', help='Config type help')
parser_commit.add_argument(
    'params', nargs='*', default=None, help='The type to add or remove')
parser_commit.set_defaults(func=commit_arguments)
