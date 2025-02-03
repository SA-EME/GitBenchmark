"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

import os
import toml
import logging

from __config__ import PATH
from config.schemas import Config


def read_config(file_path) -> Config:
    """
    Reads and parses the TOML configuration file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        Config: Parsed configuration object.

    Raises:
        ConfigError: If the file does not exist or cannot be read.
    """
    if not os.path.exists(file_path):
        logging.error("Error: Configuration file '%s' not found.", file_path)

    try:
        with open(file_path, 'r', encoding='utf8') as file:
            config_dict = toml.load(file)
    except toml.TomlDecodeError as e:
        logging.error("Error in config %s", e)
        exit(0)

    return Config(**config_dict)


CONFIG_FILE = 'config.toml'
config = read_config(os.path.join(PATH, CONFIG_FILE))
