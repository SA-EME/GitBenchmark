"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

from datetime import datetime

from utils.request import request
from utils.date import get_date

def get_latest_release(repo, default_date="2000-01-01", default_tag="0.0.0"):
    """
    Retrieves the latest release from the repository or returns default values.

    Args:
        repo (str): Repository name.
        default_date (str): Default date if no release is found.
        default_tag (str): Default version tag if no release is found.

    Returns:
        tuple: A tuple containing the published date of the latest release and its tag.
    """
    latest_release = request(f"repos/{repo}/releases/latest")

    if not latest_release:
        return datetime.strptime(default_date, "%Y-%m-%d"), default_tag
    else:
        return get_date(latest_release['published_at']), latest_release['tag_name']