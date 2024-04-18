import pathlib
from inquirer import errors

from config import get_section


def file_validator(answers, current):
    if not pathlib.Path(current).is_file():
        raise errors.ValidationError(False, reason=f"{current} is not a file")
    return True

def not_exist_validator(answers: str, current: str) -> bool:
    """Check if a scope or type exists."""
    if current in get_section('scope'):
        raise errors.ValidationError(False, reason="Scope already exist..")
    return True

def exist_validator(answers: str, current: str) -> bool:
    """Check if a scope or type exists."""
    if current in get_section('scope'):
        return True
    raise errors.ValidationError(False, reason="Scope don't exist.")
