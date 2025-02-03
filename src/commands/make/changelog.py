"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
from commands.base import BaseCommand, ROOT_COMMANDS
from datetime import datetime
from modules.commits.commit import get_filtered_commits
from modules.versioning.release import get_latest_release
from modules.versioning.manager import determine_version

from modules.changelog.generator import generate_changelog

from stacktrace import stacktrace_manager

from env import OWN_REP

class ChangelogCommand(BaseCommand):
    """
    Release command class.
    """

    COMMAND_ROOT = ROOT_COMMANDS.make

    COMMAND_NAME = 'changelog'
    COMMAND_DESCRIPTION = 'Create a new changelog entry'

    def run(self, args):
        print(f"Running changelog command with args: {args} ")
        release_date = datetime.now().strftime("%Y-%m-%d")
        published_at_date, tag_name = get_latest_release(OWN_REP)
        filtered_commits = get_filtered_commits(OWN_REP, published_at_date)
        new_version = determine_version(tag_name, filtered_commits, 'patch' or args.version)

        if not filtered_commits:
            print("No new commits found")
            return

        changelog_output = generate_changelog(new_version, release_date, filtered_commits)
        stacktrace_manager.register_action(self.full_name(), "success", content=changelog_output)

    def rollback(self):
        super().rollback()

    def register(self):
        super().register()