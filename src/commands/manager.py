"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

from commands.plugin import load_plugins


class CommandManager:
    """"
    Command manager class that handles the default commands and plugins commands.
    """
    def __init__(self):
        self.commands = {
            # TODO implement commands
        }
        self.plugins = load_plugins()

        for plugin in self.plugins.values():
            self.commands.update(plugin.register_commands())

    def run_command(self, command_name, args):
        """
        Run the command with the given name.
        """
        if command_name in self.commands:
            self.commands[command_name]["func"](args)
        else:
            print(f"Unknown command: {command_name}")
