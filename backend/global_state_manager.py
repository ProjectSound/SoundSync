from PyQt6.QtCore import QObject, pyqtSignal


class GlobalStateManager(QObject):
    _instance = None
    runningChanged = pyqtSignal(bool)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalStateManager, cls).__new__(cls)
            cls._instance._running = False
        return cls._instance

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if self._running != value:
            self._running = value
            self.runningChanged.emit(value)
