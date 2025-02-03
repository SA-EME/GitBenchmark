from enum import Enum
import re


class VERSION(Enum):
    BUILD = "build"
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"


VERSOION_PRIORITY = {
    "major": 3,
    "minor": 2,
    "patch": 1
}

def get_version_type(message, config):
    for version_type, prefixes in {
        "major": config.SemanticVersioning.major,
        "minor": config.SemanticVersioning.minor,
        "patch": config.SemanticVersioning.patch
    }.items():
        if any(message.startswith(prefix) for prefix in prefixes):
            return version_type
    return None

def get_version(message, pattern):
    """
    Get the version from the message.
    """
    match = re.search(pattern, message)
    if match:
        return match.group(2)
    return None


def get_version_by_file(file_path, pattern):
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

    filedata = re.sub(pattern, lambda m: m.group(1) + new_version, filedata)

    with open(file_path, 'w') as file:
        file.write(filedata)


def change_version(old_version: str, commit_version: str):
    """
    Change the version by commit version.
    """
    old_version = old_version.split('.')
    if commit_version == VERSION.BUILD.value:
        if len(old_version) < 4:
            old_version.append('1')
        else:
            old_version[-1] = str(int(old_version[-1]) + 1)
    elif commit_version == VERSION.PATCH.value:
        old_version[-1] = str(int(old_version[-1]) + 1)
        if len(old_version) == 4:
            old_version = old_version[:-1]
    elif commit_version == VERSION.MINOR.value:
        old_version[-2] = str(int(old_version[-2]) + 1)
        old_version[-1] = '0'
        if len(old_version) == 4:
            old_version = old_version[:-1]
    elif commit_version == VERSION.MAJOR.value:
        old_version[-3] = str(int(old_version[-3]) + 1)
        old_version[-2] = old_version[-1] = '0'
        if len(old_version) == 4:
            old_version = old_version[:-1]
    return '.'.join(old_version)


class PATTERN(Enum):
    NODE = "(\"version\"\\s*:\\s*\")([^\"]*)",
    PYTHON = "(VERSION=\")([^\"]*)\""
    # README = "(version )(\d+\.\d+\.\d+)"
