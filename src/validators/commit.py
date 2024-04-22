from inquirer import errors


def commit_message_validator(answers, current):
    """
    Return True if the commit message is not empty & don't contains single quotes or double quotes
    """
    if not current:
        raise errors.ValidationError(False, reason="Commit message can't be empty.")
    if "'" in current or '"' in current:
        raise errors.ValidationError(False, reason="Commit message can't contains single quotes or double quotes.")
    return True