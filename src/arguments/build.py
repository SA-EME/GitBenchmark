import inquirer

from config import get_section

from controllers.build import build


def build_arguments(args):
    if len(args.params) >= 1:
        scope = args.params[0]
    else:
        scope = inquirer.prompt([inquirer.Checkbox('scope',
            message="What's the scope of the commit",
            choices=get_section('scope'),
            validate=lambda _, x: len(x) > 0
        )])["scope"]

    build(scope)

