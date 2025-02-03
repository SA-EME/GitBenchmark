from utils.version import change_version, get_version_type, VERSOION_PRIORITY

from config.index import config

def determine_version(tag_name: str, commits: list, version:str = None):
    """
    Determines the new version based on commits or environment variables.

    Args:
        tag_name (str): Current version tag.
        commits (list): List of filtered commits.
        version (str, optional): Version defined in environment variables or in flag.

    Returns:
        str: The new version or None if no version change is needed.
    """
    new_version = None
    version_type = None

    if version:
        return change_version(tag_name, version)

    for commit in commits:
        current_version_type = get_version_type(commit['commit']['message'], config)
        if current_version_type:
            if (version_type is None or VERSOION_PRIORITY[current_version_type] > VERSOION_PRIORITY[version_type]):
                version_type = current_version_type

    if version_type:
        return change_version(tag_name, version_type)

    return new_version
