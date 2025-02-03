import os

from config.index import config

def generate_changelog(new_version, release_date, commits, changelog_file="CHANGELOG.md"):
    """
    Generates a changelog based on filtered commits and the new version.

    Args:
        new_version (str): New version string.
        release_date (str): Date of the release.
        filtered_commits (list): List of filtered commits.
        config (object): Project configuration.
        changelog_file (str): Path to the changelog file.

    Returns:
        str: Generated changelog content.
    """
    changelog = {key: [] for key in config.ChangeLog.Section.keys()}

    for commit in commits:
        message: str = commit['commit']['message']
        author = commit['commit']['author']['name']
        hash_commit = commit['sha']

        if '\n' in message:
            message = message.split('\n')[0]

        if not any(message.startswith(type) for type in config.ConventionalCommits.type):
            changelog["others"].append(f"{message.rstrip()} ({hash_commit}) by @{author}")

        for category, prefixes in config.ChangeLog.Section.items():
            if any(message.startswith(prefix) for prefix in prefixes):
                changelog[category].append(f"{message.rstrip()} ({hash_commit}) by @{author}")
                break

    changelog_output = f"## {new_version} - {release_date}\n"
    for category, logs in changelog.items():
        if logs:
            changelog_output += f"# {category.title()}\n"
            for log in logs:
                changelog_output += f"  - {log}\n"
            changelog_output += "\n"

    changelog_intro = config.ChangeLog.header
    if os.path.exists(changelog_file):
        with open(changelog_file, "r") as file:
            existing_content = file.read()
        new_content = changelog_intro + "\n" + changelog_output + "\n" + existing_content[len(changelog_intro):]
    else:
        new_content = changelog_intro + "\n" + changelog_output

    with open(changelog_file, "w") as file:
        file.write(new_content.rstrip())

    return changelog_output
