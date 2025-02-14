"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""
import os
import json
import logging

from datetime import datetime

from __config__ import PATH

# Default structure for the stacktrace file
DEFAULT = {
    "stacktrace": []
}


class StackTraceManager:
    """
    A class to manage logging of actions and changes (stacktrace).

    This system allows you to track every action performed by the application
    and rollback if needed.
    """

    def __init__(self, log_file='stacktrace.json'):
        """
        Initialize the StackTraceManager with a stacktrace file.

        Args:
            log_file (str): The file path where stacktrace will be saved.
            Defaults to 'stacktrace.json'.
        """
        self.log_file = os.path.join(os.getcwd(), PATH, log_file)
        self.logs = self._load_stacktrace()

    def _load_stacktrace(self):
        """
        Load stacktrace from the stacktrace file.

        Returns:
            dict: The stacktrace loaded from the file,
            or default stacktrace if the file doesn't exist or is invalid.
        """
        try:
            with open(self.log_file, 'r', encoding='utf8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return DEFAULT
        except FileNotFoundError:
            return DEFAULT

    def _save_stacktrace(self):
        """
        Save the current stacktrace to the log file.
        """
        with open(self.log_file, 'w', encoding='utf8') as file:
            json.dump(self.logs, file, indent=4)

    def register_action(self, command, status, content=None):
        """
        Register a new log entry to the stacktrace.

        Args:
            command (str): The command or action that was executed.
            status (str): The result status of the action (e.g., 'success', 'error').
            content (str, optional): Additional content or information about the log entry.
            category (str, optional): Type or category of the log (e.g., 'versioning', 'rollback').
        """
        log_entry = {
            "command": command,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        if content:
            log_entry["content"] = content

        # Ensure the stacktrace exists in the logs and add the new log entry
        if 'stacktrace' not in self.logs:
            self.logs["stacktrace"] = []
        self.logs["stacktrace"].append(log_entry)
        self._save_stacktrace()

    def get_actions_by_command(self, command):
        """
        Retrieve all log entries corresponding to a specific command/action.

        Args:
            command (str): The command to filter the logs.

        Returns:
            list: A list of log entries that match the command.
        """
        return [log for log in self.logs["stacktrace"] if log["command"] == command]

    def undo_last_action(self):
        """
        Undo the last action recorded in the stacktrace.

        Returns:
            dict: The last log entry that was undone, or None if the stacktrace is empty.
        """
        if not self.logs["stacktrace"]:
            logging.info("No changes to undo.")
            return None

        last_log = self.logs["stacktrace"].pop()
        self._save_stacktrace()
        return last_log

    def get_all_actions(self):
        """
        Retrieve all actions recorded in the stacktrace.

        Returns:
            list: A list of all log entries in the stacktrace.
        """
        return self.logs["stacktrace"]


# Initialize the StackTraceManager
stacktrace_manager = StackTraceManager()
