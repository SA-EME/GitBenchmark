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


def read_config(file_path) -> Config|None:
    """
    Reads and parses the TOML configuration file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        Config: Parsed configuration object.

    Raises:
        ConfigError: If the file does not exist or cannot be read.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                config_dict = toml.load(file)
                return Config(**config_dict)
        except toml.TomlDecodeError as e:
            logging.error("Error in config %s", e)
            exit()
    else :
        logging.warning("Configuration file '%s' not found.", file_path)

    return None

def save_config(config):
    """
    Save the current configuration to the TOML file.
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf8') as file:
            toml.dump(config, file)
        logging.info("Configuration saved successfully.")
    except Exception as e:
        logging.error("Failed to save configuration: %s", e)

def update_config(section: str, key: str, value):
    """
    Update any section/key in the configuration and save it safely.

    Args:
        section (str): The section to update.
        key (str): The key within the section.
        value (Any): The new value to set.
    """
    config = read_config(CONFIG_FILE)

    config_dict = config.dict()

    keys = section.split(".")
    sub_config = config_dict
    for k in keys:
        if k not in sub_config or not isinstance(sub_config[k], dict):
            sub_config[k] = {}
        sub_config = sub_config[k]

    sub_config[key] = value

    logging.info("Updated configuration: %s.%s = %s", section, key, value)

    try:
        # updated_config = config.copy(update=config_dict) 
        save_config(config_dict)
    except Exception as e:
        logging.error("Failed to save configuration: %s", e)

CONFIG_FILE = os.path.join(PATH, 'config.toml')
config = read_config(CONFIG_FILE)
