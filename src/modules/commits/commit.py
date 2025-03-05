"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

from datetime import datetime

from utils.request import request
from utils.date import get_date

from env import OWN_REP

def get_filtered_commits(repo = OWN_REP, since_date=datetime.strptime('2000-01-01','%Y-%m-%d')):
    """
    Retrieves and filters commits after a specific date.

    Args:
        repo (str): Repository name.
        since_date (datetime): The date to filter commits from.

    Returns:
        list: A list of filtered commits after the specified date.
    """
    commits = request(f"repos/{repo}/commits")
    return [commit for commit in commits if get_date(commit['commit']['committer']['date']) > since_date]
