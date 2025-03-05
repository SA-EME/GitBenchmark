"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import logging
from datetime import datetime
from env import OWN_REP
from cmd.base import BaseCommand, ROOT_COMMANDS


from modules.commits.commit import get_filtered_commits
from modules.versioning.release import get_latest_release
from modules.versioning.manager import determine_version
from modules.changelog.generator import generate_changelog
from utils.version import get_version_by_file, replace_version

import subprocess


from config.index import CONFIG_FILE

class ReleaseMakeCommand(BaseCommand):
    """
    Release command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'release'
    COMMAND_DESCRIPTION = 'Release a new version of the project'
    COMMAND_ARGS = [
        {"name": "version", "help": "The version to release"}
    ]
    # COMMAND_FLAGS = [
    #     {"name": "--minor", "action": "store_true", "help": "Increment the minor version"},
    #     {"name": "--major", "action": "store_true", "help": "Increment the major version"}
    # ]

    def change_version(self, files, new_version):
        for key, value in files.items():
            path = value["path"]
            pattern = value["pattern"]
            old_version: str = get_version_by_file(path, pattern)
            if old_version is None:
                logging.warning(f"[red]Can't find version in {path} with pattern {pattern}[/red]")
                continue
            replace_version(path, pattern, new_version)


        replace_version(CONFIG_FILE, '(version=\")([^\"]*)', new_version)

    def run(self, args):
        version = self.config.Application.version
        files = self.config.Version.Files

        release_date = datetime.now().strftime("%Y-%m-%d")
        published_at_date, remote_version = get_latest_release(OWN_REP)
        filtered_commits = get_filtered_commits(OWN_REP, published_at_date)
        new_version = determine_version(version, filtered_commits)

        self.change_version(files, new_version)
        generate_changelog(new_version, release_date, filtered_commits)

        subprocess.run(f"git commit -m 'release: ${new_version}'", shell=True, check=True)

        if (version != remote_version[1]):
            logging.warning("Different version between local & remote %s - %s", version, remote_version[1])


    def rollback(self):
        print("Rolling back the release...")

    def register(self):
        print("Registering release command...")
