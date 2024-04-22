import inquirer
from config import get_section
from version import VERSION
from controllers.type import add, remove, show

def type_arguments(args):
    if args.action == 'add':
        if len(args.params) >= 1:
            name = args.params[0]
        else:
            name = inquirer.prompt([inquirer.Text('name', message="What's the name of the new type ?", validate=lambda _, c: c <= 16)])["name"]

        if len(args.params) >= 2:
            version = args.params[1]
        else:
            version = inquirer.prompt([inquirer.List('version', message="What's the version of this type ?", choices=list(VERSION))])["version"]

        add(name, version)
    elif args.action == 'remove':
        if len(args.params) >= 1:
            name = args.params[0]
        else:
            name = inquirer.prompt([inquirer.List('name', message="What's the name of the type ?", choices=get_section("type"))])["name"]
        remove(name)
    elif args.action == 'list':
        show()