from env import PLATFORM
from datetime import datetime

def get_date(_date: str) -> datetime:
    """
    Get the date by platform type.
    Example of date:
    - GITEA: 2024-09-24T10:47:21+02:00
    - GITHUB: 2024-10-01T13:00:10Z
    """

    date: str = None

    if PLATFORM == "GITEA":
        date = _date[:-6]
    elif PLATFORM == "GITHUB":
        date = _date[:-1]

    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")