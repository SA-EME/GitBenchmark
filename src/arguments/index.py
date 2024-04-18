import argparse


from arguments.scope import scope_arguments

parser = argparse.ArgumentParser(description="A command-line tool to help you to have compliance with your commit & easy the versioning.")
subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

# create the parser for the "config scope" command
parser_scope = subparsers.add_parser('scope', help='Config scope help')
parser_scope.add_argument('action', choices=['add', 'remove', 'list'], help='The action to perform on the scope')
parser_scope.add_argument('params', nargs='*', default=None, help='The scope to add or remove')
parser_scope.set_defaults(func=scope_arguments)



