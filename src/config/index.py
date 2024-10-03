"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

import os
import toml

from config.schemas import Config


class ConfigError(Exception):
    """Custom exception for configuration errors."""


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
        raise ConfigError(f"Error: Configuration file '{file_path}' not found.")

    try:
        with open(file_path, 'r', encoding='utf8') as file:
            config_dict = toml.load(file)
    except toml.TomlDecodeError:
        raise ConfigError(f"Error: Failed to parse the TOML file '{file_path}'.")

    return Config(**config_dict)


CONFIG_FILE = '.gitbenchmark'
config = read_config(CONFIG_FILE)