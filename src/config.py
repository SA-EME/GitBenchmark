import os
import toml
from rich import print

CONFIG_FILES = ['.gitbenchmark', '.gb', '.gitbenchmark.toml', '.gb.toml']

DEFAULT_CONFIG = {
    "type": {
        "release": {
            "version": "major"
        },
        "breaking": {
            "version": "major"
        },
        "feat": {
            "version": "minor"
        },
        "chore": {
            "version": "patch"
        },
        "fix": {
            "version": "patch"
        },
        "ci": {
            "version": "patch"
        },
        "docs": {
            "version": "patch"
        },
        "perf": {
            "version": "patch"
        },
        "refactor": {
            "version": "patch"
        },
        "style": {
            "version": "patch"
        },
        "test": {
            "version": "patch"
        }
    },
    "scope": {
        "project": {}
    }
}

def create_config() -> None:
    """Crée un fichier de configuration avec les valeurs par défaut."""
    with open('.gitbenchmark', 'w') as file:
        toml.dump(DEFAULT_CONFIG, file)

def init_config() -> str:
    """Initialise la configuration en cherchant le fichier de configuration existant."""
    for f in CONFIG_FILES:
        if os.path.isfile(f):
            return f
    return None

def load_config(config_path: str) -> dict:
    """Charge la configuration à partir du fichier spécifié."""
    try:
        with open(config_path, "r") as file:
            return toml.load(file)
    except toml.TomlDecodeError as error:
        print(f"[red]Impossible de charger le fichier de configuration, chemin {config_path} [/red]")
        print(f"[red]Erreur : {error}[/red]")
        return None

config_path = init_config()
config = load_config(config_path) if config_path else None

def get_subsection(prefix: str) -> list:
    """Récupère une sous-section de la configuration."""
    keys = prefix.split('.')
    subsection = config
    for k in keys:
        if isinstance(subsection, dict):
            subsection = subsection.get(k)
        else:
            return []
    return list(subsection.keys())

def get_section(section: str) -> list:
    """Récupère une section de la configuration."""
    return list(config[section].keys())

def remove_section(section: str) -> None:
    """Supprime une section du fichier de configuration."""
    keys = section.split('.')
    last_key = keys.pop()
    temp = config
    for k in keys:
        if k not in temp:
            print(f"Section '{section}' non trouvée dans le fichier de configuration.")
            return
        temp = temp[k]
    if last_key in temp:
        del temp[last_key]
        with open(config_path, 'w') as f:
            toml.dump(config, f)
    else:
        print(f"Section '{section}' non trouvée dans le fichier de configuration.")

def get_value(key: str):
    """Récupère une valeur du fichier de configuration."""
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, [])
        else:
            return []
    return value

def set_value(key: str, value) -> None:
    """Définit une valeur dans le fichier de configuration."""
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
