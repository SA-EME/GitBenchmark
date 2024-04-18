import inquirer
from controllers.scope import add, remove, show, modify
from validators.scope import file_validator, exist_validator, not_exist_validator
from config import get_section
from version import PATTERN

def scope_arguments(args):
    if args.action == 'add':
        if len(args.params) >= 1:
            name = args.params[0]
        else:
            name = inquirer.prompt([inquirer.Text('name', message="What's the name of the scope ?", validate=not_exist_validator)])["name"]

        if len(args.params) >= 2:
            path = args.params[1]
        else:
            path = inquirer.prompt([inquirer.Text('path', message="What's the main file of this scope ?", validate=file_validator)])["path"]

        if len(args.params) >= 3:
            pattern = args.params[2]
        else:
            pattern = inquirer.prompt([inquirer.List('pattern', message="What's the main file of this scope ?", choices=list(PATTERN))])["pattern"]

        add(name, path, pattern)
    elif args.action == 'remove':
        if len(args.params) >= 1:
            name = args.params[0]
        else:
            name = inquirer.prompt([inquirer.List('name', message="What's the name of the scope ?", choices=get_section("scope"))])["name"]
        remove(name)
    elif args.action == 'list':
        show()