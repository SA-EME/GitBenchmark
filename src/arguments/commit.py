import inquirer
from controllers.commit import commit
from validators.commit import commit_message_validator
from config import get_section

from utils.git import check_commit


def commit_arguments(args):

    if not check_commit() and args.command == 'commit':
        return

    if len(args.params) >= 1:
        type = args.params[0]
    else:
        type = inquirer.prompt([inquirer.List('type',
                                              message="What commit do you wan't to do?",
                                              choices=get_section('type'))])["type"]

    if len(args.params) >= 2:
        scope = args.params[1]
    else:
        scope = inquirer.prompt([inquirer.Checkbox('scope',
                                                   message="What's the scope of the commit",
                                                   choices=get_section(
                                                       'scope'),
                                                   validate=lambda _, x: len(
                                                       x) > 0
                                                   )])["scope"]

    if len(args.params) >= 3:
        message = args.params[2]
    else:
        message = []
        for sc in scope:
            message_question = inquirer.Text('message', message=f"What's the message of the commit for {sc}",
                                             validate=commit_message_validator)
            message_answer = inquirer.prompt([message_question])
            message.append(str(message_answer['message']).strip())

    commit(args.command, type, scope, message)
