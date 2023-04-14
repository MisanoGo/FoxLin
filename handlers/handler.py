import os

from config.settings import AUTO_RUNNING_TESTS


class SystemHandler(object):
    """
    Handler system for reading settings configuration
    file, and set some arguments and commands for main.py
    file, for easy usage.
    """
    auto_running_tests = AUTO_RUNNING_TESTS

    def check_command_handlers(self):
        if self.auto_running_tests:
            os.system("pytest")
            return 1


system_handler = SystemHandler()
