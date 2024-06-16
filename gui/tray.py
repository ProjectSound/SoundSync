from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu


class Tray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setIcon(QIcon(":/app_icon.ico"))
        self.setToolTip("SilentGuardian")
        self.menu = QMenu()

        self.show_action = QAction("Show", self)
        self.quit_action = QAction("Quit", self)

        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.show_action.triggered.connect(self.show_window)
        self.quit_action.triggered.connect(QApplication.instance().quit)

        self.setContextMenu(self.menu)
        self.activated.connect(self.tray_activated)

    def show_window(self):
        self.parent.show()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()
