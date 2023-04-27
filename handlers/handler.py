import subprocess
import os

from config.settings import AUTO_RUNNING_TESTS, BASE_DIR


class SystemHandler(object):
    """
    Handler system for reading settings configuration
    file, and set some arguments and commands for main.py
    file, for easy usage.
    """
    auto_running_tests = AUTO_RUNNING_TESTS

    def check_command_handlers(self):
        if self.auto_running_tests:
            subprocess.Popen(["pytest"])
            return 1
        else:
            print('No automation tool enabled, you can configure it from config.settings')
            return 1

    def make_docs(self):
        os.chdir(os.path.join(BASE_DIR, 'documents'))
        subprocess.Popen(["make", "html"], stdout=subprocess.DEVNULL)
        return 1

system_handler = SystemHandler()
