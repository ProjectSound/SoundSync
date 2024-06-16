import sys

from PyQt6.QtWidgets import QApplication

from backend.actions import Actions
from backend.audio_core import InputManager, InputDeviceManager, AudioSessionManager, SoundManager
from backend.binds import Binds
from backend.config import Config
from backend.cutoff import CutOff
from backend.global_state_manager import GlobalStateManager
from backend.logger import Logger
from backend.settings import Settings
from gui.custom_messagebox import CustomMessageBox
from gui.main_window import MainWindow


class Core:
    def __init__(self, debug=False, args=None):
        self.run = None
        self.is_silent = None

        self.check_args(args)

        self.logger = Logger()
        self.logger.log("Core", "Application started")
        self.window = None
        self.config = Config()
        self.input_device_manager = InputDeviceManager()
        self.audio_session_manager = AudioSessionManager()
        self.sound_manager = SoundManager(self.config.selectedApp)
        self.cutoff = CutOff(self.sound_manager, debug)
        self.sound_manager.set_cutoff_run(self.cutoff.run)
        self.input_manager = InputManager(self.cutoff, debug)
        self.actions = Actions(self, self.sound_manager, self.cutoff, self.input_manager, debug)
        self.binds = Binds(self.actions, debug)
        self.binds.load()
        self.settings = Settings(debug)

        self.input_manager.create(self.config.selectedInput1, self.config.threshold1,
                                  self.config.threshold_not_reached1, True)

        if self.config.selectedInput2 is not None:
            self.input_manager.create(self.config.selectedInput2, self.config.threshold2,
                                      self.config.threshold_not_reached2, False)

        self.cutoff.set(self.config.selectedCutoff)

        self.state_manager = GlobalStateManager()

        if self.run:
            self.state_manager.running = True
            self.handle_running_changed()

        self.start_ui()

    def start_ui(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(app, self, self.actions, self.binds, self.cutoff, self.input_device_manager,
                                 self.audio_session_manager, self.input_manager, self.sound_manager.update_process,
                                 self.settings, self.is_silent)
        sys.exit(app.exec())

    def check_args(self, args):
        self.is_silent = "-silent" in args
        self.run = "-run" in args

    def handle_running_changed(self):
        try:
            if self.state_manager.running:
                self.input_manager.start_all()
                self.logger.log("Core", "Change running state: True")
            else:
                self.input_manager.stop_all()
                self.logger.log("Core", "Change running state: False")
        except Exception as e:
            self.logger.log("Core", str(e))
            CustomMessageBox(0, str(e),
                             [['Ok', 'blue', None]])
