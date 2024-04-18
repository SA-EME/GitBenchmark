from enum import Enum
import re

class VERSION(Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"
    
def get_version(file_path, pattern):
    """
    Get the version from the file.
    """
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                return match.group(2)
    return None

def replace_version(file_path, pattern, new_version):
    """
    Replace the version in the file.
    """
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = re.sub(pattern, lambda m: m.group(1) + new_version + '"', filedata)

    with open(file_path, 'w') as file:
        file.write(filedata)

def change_version(old_version: str, commit_version: str):
    """
    Change the version by commit version.
    """
    old_version = old_version.split('.')
    if commit_version == VERSION.PATCH.value:
        old_version[-1] = str(int(old_version[-1]) + 1)
    elif commit_version == VERSION.MINOR.value:
        old_version[-2] = str(int(old_version[-2]) + 1)
        old_version[-1] = '0'
    elif commit_version == VERSION.MAJOR.value:
        old_version[-3] = str(int(old_version[-3]) + 1)
        old_version[-2] = old_version[-1] = '0'
    return '.'.join(old_version)

class PATTERN(Enum):
    NODE = "(\"version\"\\s*:\\s*\")([^\"]*)\"",
    PYTHON = '(VERSION=")([^"]*)"'
