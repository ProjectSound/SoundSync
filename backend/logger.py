import atexit
import datetime
import os


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            cls._instance.log_file = f"logs/app_log_{timestamp}.txt"
            atexit.register(cls._instance.save_logs_on_exit)
            cls._instance.create_logs_folder()
        return cls._instance

    def create_logs_folder(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def log(self, class_name, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{class_name}] {message}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)

    def save_logs_on_exit(self):
        self.log("Logger", "Application exited")