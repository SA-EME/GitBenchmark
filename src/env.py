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

dotenv_path = os.path.join(os.getcwd(), '.env')
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

LOG_LEVEL: str = get_env("LOG_LEVEL", True, "INFO", str)
LOG_FILE: str = get_env("LOG_FILE", False, None, str)
