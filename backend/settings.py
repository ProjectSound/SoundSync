import os
import sys
import subprocess

from backend.config import Config
from backend.logger import Logger


class Settings:
    def __init__(self, debug):
        self.config = Config()
        self.logger = Logger()
        self.debug = debug
        if getattr(sys, 'frozen', False):
            self.app_mode = 'exe'
            self.file_path = sys.executable
        else:
            self.app_mode = 'py'
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.file_path = os.path.join(parent_dir, "main.py")
        self.startup_status = self.check_task_exists('SilentGuardian')
        self.config.auto_launch = self.startup_status
        self.config.save()

    @staticmethod
    def check_task_exists(task_name) -> bool:
        command = ["schtasks", "/Query", "/TN", task_name]

        result = subprocess.run(command, capture_output=True, text=True, encoding='latin1', shell=True)
        return result.returncode == 0

    def create_task_in_task_scheduler(self, task_name, script_path):
        command = [
            "schtasks",
            "/Create",
            "/SC", "ONLOGON",
            "/DELAY", "0000:10",
            "/TN", task_name,
            "/TR", f'"{script_path}" -silent -run',
            "/RL", "HIGHEST",
            "/F"
        ]

        result = subprocess.run(command, capture_output=True, text=True, encoding='latin1', shell=True)
        if self.debug:
            if result.returncode == 0:
                print("Task created successfully.")
            else:
                print(f"Failed to create task. Error: {result.stderr}")

    def delete_task_from_task_scheduler(self, task_name):
        command = ["schtasks", "/Delete", "/TN", task_name, "/F"]

        result = subprocess.run(command, capture_output=True, text=True, encoding='latin1', shell=True)
        if self.debug:
            if result.returncode == 0:
                print("Task deleted successfully.")
            else:
                print(f"Failed to delete task. Error: {result.stderr}")

    def add_to_startup(self):
        if self.startup_status:
            if self.debug:
                print("The application is already in autostart")
            self.logger.log("Settings", "The application is already in autostart")
            return

        executable_path = self.file_path

        if self.app_mode == "py":
            executable_path = f"python {self.file_path}"

        self.create_task_in_task_scheduler("SilentGuardian", executable_path)
        if self.debug:
            print("Application added to autostart with Task Scheduler")
        self.logger.log("Settings", "Application added to autostart with Task Scheduler")
        self.startup_status = True
        self.config.auto_launch = True
        self.config.save()

    def remove_from_startup(self):
        if not self.startup_status:
            if self.debug:
                print("The application is not in autostart")
            self.logger.log("Settings", "The application is not in autostart")
            return

        self.delete_task_from_task_scheduler("SilentGuardian")
        if self.debug:
            print("Application removed from autostart with Task Scheduler")
        self.logger.log("Settings", "Application removed from autostart with Task Scheduler")
        self.startup_status = False
        self.config.auto_launch = False
        self.config.save()
