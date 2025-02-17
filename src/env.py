"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import sys

import logging

from dotenv import load_dotenv

from __config__ import PATH


DEFAULT_ENV = """# Log
LOG_LEVEL=WARN
LOG_FILE=None

# Repository
PLATFORM=github
TOKEN=YOUR_TOKEN
URL=https://api.github.com
OWNER=OWNER
REPO=REPO
"""

dotenv_path = os.path.join(os.getcwd(), PATH, '.env')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)


def get_env(key: str, required=False, default=None, cast=None, **kwargs):
    """
    load .env configuration in variable environement system
    return 1: loaded dotenv file
    return 0: can't load dotenv file
    """
    seperator = kwargs.get("seperator", None)
    transform = kwargs.get("transform", None)
    if (value := os.environ.get(key)) is None:
        if required is True:
            if default is not None:
                return default

            logging.error("Missing required environment variable %s", key)
            sys.exit(1)
        else:
            return None

    if transform is not None:
        value = transform(value)

    if cast is not None:
        if cast is list:
            return value.split(seperator)
        try:
            return cast(value)
        except (ValueError, TypeError):
            logging.error("Invalid value for environment variable %s", key)
            sys.exit(1)
    return value


LOG_LEVEL: str = get_env("LOG_LEVEL", True, "ERROR", str)
LOG_FILE: str = get_env("LOG_FILE", False, None, str)

PLATFORM: str = get_env("PLATFORM", True, "", str).upper()
TOKEN: str = get_env("TOKEN", True, "", str)
URL: str = get_env("URL", True, "", str)
OWNER: str = get_env("OWNER", True, "", str)
REPO: str = get_env("REPO", True, "", str)

OWN_REP: str = f"{OWNER}/{REPO}"
