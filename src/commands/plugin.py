"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import sys
import logging

import importlib.util


class GBPlugin:
    """
    Base class for plugins.
    This class should be inherited by all plugins.
    """

    def __init__(self):
        self.name = None
        self.description = None

    def register_commands(self):
        """
        Register the commands for the plugin.
        """
        raise NotImplementedError


def load_plugins(plugin_directory="plugins") -> dict[str, GBPlugin]:
    """
    Load all plugins from the given directory.
    """
    plugins = {}

    # Get the path of the plugins directory
    plugins_path = os.path.join(os.getcwd(), plugin_directory)

    if not os.path.exists(plugins_path):
        logging.info("Le répertoire des plugins %s n'existe pas.", plugins_path)
        return plugins

    # Load all plugins from the directory
    for plugin_name in os.listdir(plugins_path):
        plugin_path = os.path.join(plugins_path, plugin_name)
        if os.path.isdir(plugin_path):
            module_name = f"{plugin_name}.command"

            # Load the plugin module
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(plugin_path, "command.py"))
                module = importlib.util.module_from_spec(spec)

                try:
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                except FileNotFoundError as e:
                    logging.error("Erreur lors du chargement du plugin %s: %s", plugin_name, e)
                    continue

                # Find the plugin class which inherits from PluginBase
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and issubclass(attr, GBPlugin) and attr is not GBPlugin):
                        plugin_class = attr
                        break

                if plugin_class is not None:
                    plugin_instance = plugin_class()
                    plugins[plugin_instance.name] = plugin_instance
                    logging.debug("Plugin %s chargé avec succès !", plugin_instance.name)
                else:
                    logging.warning("Aucune classe héritant de GBPlugin trouvée dans le plugin %s",
                                    plugin_name)

            except ModuleNotFoundError as e:
                logging.error("Erreur lors du chargement du plugin %s: %s", plugin_name, e)
                sys.exit(1)

    return plugins
