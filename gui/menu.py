from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from backend.config import Config
from gui.svg_color_widget import SVGColorWidget


class Menu(QWidget):
    switchTab = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.config = Config()

        self.width = int(250 * self.config.scale[self.config.selectedScale]['scale'])
        self.height = int(82 * self.config.scale[self.config.selectedScale]['scale'])

        self.iconSize = int(28 * self.config.scale[self.config.selectedScale]['scale'])

        self.setFixedWidth(self.width)
        self.initUI()

        self.lastTab = 0

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # INPUT #

        self.input = QWidget()

        self.input.setFixedSize(self.width, self.height)
        inputLayout = QVBoxLayout()
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/input.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Select input to listen")
        label.setContentsMargins(0, 0, 0, 5)
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)

        inputLayout.addWidget(iconContainerWidget)

        self.input.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']}; border-radius: 10px;")

        self.input.mousePressEvent = partial(self.emitSignal, index=0)

        # APP #

        self.app = QWidget()

        self.app.setFixedSize(self.width, self.height)
        appLayout = QVBoxLayout()
        appLayout.setContentsMargins(0, 0, 0, 0)
        appLayout.setSpacing(0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/app.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Select app to control")
        label.setContentsMargins(0, 0, 0, 5)
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)

        appLayout.addWidget(iconContainerWidget)

        self.app.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")

        self.app.mousePressEvent = partial(self.emitSignal, index=2)

        # CUTOFF #

        self.cutoff = QWidget()

        self.cutoff.setFixedSize(self.width, self.height)
        cutoffLayout = QVBoxLayout()
        cutoffLayout.setContentsMargins(0, 0, 0, 0)
        cutoffLayout.setSpacing(0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/cutoff.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Cutoff mode")
        label.setContentsMargins(0, 0, 0, 5)
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)

        cutoffLayout.addWidget(iconContainerWidget)

        self.cutoff.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")

        self.cutoff.mousePressEvent = partial(self.emitSignal, index=4)

        # BINDS #

        self.binds = QWidget()

        self.binds.setFixedSize(self.width, self.height)
        bindsLayout = QVBoxLayout()
        bindsLayout.setContentsMargins(0, 0, 0, 0)
        bindsLayout.setSpacing(0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/binds.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Binds")
        label.setContentsMargins(0, 0, 0, 5)
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)

        bindsLayout.addWidget(iconContainerWidget)

        self.binds.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")

        self.binds.mousePressEvent = partial(self.emitSignal, index=5)

        # SETTINGS #

        self.settings = QWidget()

        self.settings.setFixedSize(self.width, self.height)
        settingsLayout = QVBoxLayout()
        settingsLayout.setContentsMargins(0, 0, 0, 0)
        settingsLayout.setSpacing(0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/settings.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Settings")
        label.setContentsMargins(0, 0, 0, 5)
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)

        settingsLayout.addWidget(iconContainerWidget)

        self.settings.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")

        self.settings.mousePressEvent = partial(self.emitSignal, index=9)

        # SETUP EVERYTHING #

        widget = QWidget()
        self.input.setLayout(inputLayout)
        self.app.setLayout(appLayout)
        self.cutoff.setLayout(cutoffLayout)
        self.binds.setLayout(bindsLayout)
        self.settings.setLayout(settingsLayout)

        layout.addWidget(self.input)
        layout.addWidget(self.app)
        layout.addWidget(self.cutoff)
        layout.addWidget(self.binds)
        layout.addWidget(self.settings)

        widget.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(widget)

        self.setLayout(main_layout)

    def emitSignal(self, event, index):
        if self.lastTab == 0:
            self.input.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        elif self.lastTab == 2:
            self.app.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        elif self.lastTab == 4:
            self.cutoff.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        elif self.lastTab == 5:
            self.binds.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        elif self.lastTab == 9:
            self.settings.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")

        self.lastTab = index

        if index == 0:
            self.input.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};"
                                     f"border-radius: 10px;")
        elif index == 2:
            self.app.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};"
                                   f"border-radius: 10px;")
        elif index == 4:
            self.cutoff.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};"
                                      f"border-radius: 10px;")
        elif index == 5:
            self.binds.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};"
                                     f"border-radius: 10px;")
        elif index == 9:
            self.settings.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};"
                                        f"border-radius: 10px;")

        self.switchTab.emit(index)
