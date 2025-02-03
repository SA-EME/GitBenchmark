from utils.request import request
from utils.date import get_date

def get_filtered_commits(repo, since_date):
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
