import os
import toml

from rich import print

config_file = ['.gitbenchmark', '.gitbenchmark.toml', '.gb', '.gb.toml' ]
# TODO : change path to correspond to the root of the project
default_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.toml")

config_path = default_config_file

def init_config():
    global config_path, config_file
    for file in config_file:
        if os.path.isfile(file):
            config_path = file
            break

    try:
        with open(config_path, "r") as file:
            toml.load(file)
    except toml.TomlDecodeError as error:
        print(f"[red]can't load config file, path {config_path} [/red]")
        print(f"[red]error: {error}[/red]")


def get_section(section):
    global config_path
    config = toml.load(config_path)
    return list(config[section].keys())


def remove_section(section):
    """
    Remove a section from the config file
    """
    global config_path
    config = toml.load(config_path)

    keys = section.split('.')
    last_key = keys.pop()
    temp = config

    for k in keys:
        if k not in temp:
            print(f"Section '{section}' not found in the config file.")
            return
        temp = temp[k]

    if last_key in temp:
        del temp[last_key]

        with open(config_path, 'w') as f:
            toml.dump(config, f)
    else:
        print(f"Section '{section}' not found in the config file.")


def get_value(key):
    """
    Get a value from the config file
    """
    global config_path
    config = toml.load(config_path)
    return config.get(key, [])


def set_value(key: str, value):
    """
    Set a value in the config file
    """
    global config_path
    config = toml.load(config_path)

    keys = key.split('.')
    last_key = keys.pop()
    temp = config

    for k in keys:
        if k not in temp:
            temp[k] = {}
        temp = temp[k]

    temp[last_key] = value

    with open(config_path, 'w') as f:
        toml.dump(config, f)

