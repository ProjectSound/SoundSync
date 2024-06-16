import math

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QPushButton, QSizePolicy, QLabel

from backend.config import Config


class Binds(QWidget):
    switchTab = pyqtSignal(int)
    showBindRemove = pyqtSignal(int)

    def __init__(self, actions, binds):
        super().__init__()

        self.config = Config()

        self.binds_core = binds

        self.buttonHeight = int(32 * self.config.scale[self.config.selectedScale]['scale'])

        self.lastSelectedBind = None
        self.selectedBind = None

        self.actions = actions

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # layout.setContentsMargins(10, 0, 8, 10)

        bottomMargin = 0

        if self.config.selectedScale == 1:
            bottomMargin = 5
        elif self.config.selectedScale == 2:
            bottomMargin = 7
        elif self.config.selectedScale == 3:
            bottomMargin = 9
        elif self.config.selectedScale == 4:
            bottomMargin = 11
        else:
            bottomMargin = 0

        layout.setContentsMargins(8, 0, 8, bottomMargin)

        # BINDS LIST #

        self.binds = QWidget()
        self.bindsLayout = QVBoxLayout(self.binds)
        self.bindsLayout.setContentsMargins(5, 0, 5, 0)
        self.bindsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bindsLayout.setSpacing(5)

        header = QLabel("Binds:")
        header.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        header.setContentsMargins(5, 0, 0, 0)

        if len(self.binds_core.get().items()) == 0:
            self.addBindWidget(-1, "No binds, create one!", "")

        for key, value in self.binds_core.get().items():
            for combination, action in value.items():
                self.addBindWidget(key, combination, action)

        # SCROLL AREA #

        scroll_area = QScrollArea()
        scrollSize = int(6 * self.config.scale[self.config.selectedScale]['scale'])
        scroll_area.setStyleSheet(f"""
                    QScrollArea{{
                        border: none;
                    }}
                    QScrollBar {{
                        background: {self.config.colorMode[self.config.selectedTheme]['scrollBackground']};
                        width: {scrollSize}px;
                        border-radius: {math.floor(scrollSize / 2)}px;
                    }}
                    QScrollBar::handle {{
                        background: {self.config.colorMode[self.config.selectedTheme]['scrollHandle']};
                        border-radius: {math.floor(scrollSize / 2)}px;
                    }}
                    QScrollBar::add-page, QScrollBar::sub-page {{
                        background: none;
                    }}
                    QScrollBar::add-line, QScrollBar::sub-line {{
                        height: 0px;
                    }}
                """)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.binds)

        # BUTTONS #

        buttons = QWidget()
        buttonsLayout = QHBoxLayout(buttons)

        addButton = QPushButton("Add")
        addButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(addButton)

        self.removeButton = QPushButton("Remove")
        self.removeButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(self.removeButton)
        self.removeButton.setDisabled(True)

        clearButton = QPushButton("Clear")
        clearButton.setFixedHeight(self.buttonHeight)
        clearButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.apply_button_styles(clearButton)

        buttonsLayout.addWidget(addButton)
        buttonsLayout.addWidget(self.removeButton)
        buttonsLayout.addWidget(clearButton)

        addButton.clicked.connect(lambda: self.switchTab.emit(6))
        self.removeButton.clicked.connect(self.emitRemoveBind)
        clearButton.clicked.connect(self.showClearBinds)

        buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        buttonsLayout.setContentsMargins(5, 0, 11, 9)

        # COMBINE EVERYTHING #

        layout.addWidget(header)
        layout.addWidget(scroll_area)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def addBindWidget(self, key, combination, action):
        bind_widget = QWidget()
        bind_widget.setObjectName(f"BindWidget_{key}")
        bind_widget.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
        bind_layout = QHBoxLayout(bind_widget)
        bind_widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                                  f"border-radius: 5px;")

        keybindLabel = QLabel(str(combination))
        keybindLabel.setObjectName("Keybind")
        keybindLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")

        actionLabel = QLabel(str(action))
        actionLabel.setObjectName("Action")
        actionLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
        actionLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        bind_layout.addWidget(keybindLabel)
        bind_layout.addWidget(actionLabel)

        if key != -1:
            bind_widget.installEventFilter(self)

        self.bindsLayout.addWidget(bind_widget)

    def createBind(self):
        if len(self.binds_core.get().items()) == 1:
            widget = self.getWidgetByName(f"BindWidget_-1")
            if widget:
                widget.deleteLater()

        last_key = list(self.binds_core.get().keys())[-1]
        last_item = self.binds_core.get()[last_key]
        combination, action = list(last_item.items())[0]
        self.addBindWidget(last_key, combination, action)

    def removeBind(self):
        widget = self.getWidgetByName(f"BindWidget_{self.lastSelectedBind}")
        widget.deleteLater()
        self.binds_core.remove(self.lastSelectedBind)
        if len(self.binds_core.get().items()) == 0:
            self.addBindWidget(-1, "No binds, create one!", "")

    def clearBinds(self):
        self.binds_core.clear()
        while self.bindsLayout.count():
            item = self.bindsLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.addBindWidget(-1, "No binds, create one!", "")

    def emitRemoveBind(self):
        if self.selectedBind is not None:
            self.lastSelectedBind = self.selectedBind
            self.showBindRemove.emit(self.selectedBind)
            widget = self.getWidgetByName(f"BindWidget_{self.selectedBind}")
            widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
            keybind = widget.findChild(QLabel, "Keybind")
            action = widget.findChild(QLabel, "Action")
            keybind.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")
            action.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
            self.selectedBind = None
            self.removeButton.setDisabled(True)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def showClearBinds(self):
        if not self.selectedBind == None:
            widget = self.getWidgetByName(f"BindWidget_{self.selectedBind}")
            widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                f"border-radius: 5px;")
            keybind = widget.findChild(QLabel, "Keybind")
            action = widget.findChild(QLabel, "Action")
            keybind.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")
            action.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
            self.selectedBind = None
        self.removeButton.setDisabled(True)
        self.switchTab.emit(8)

    def getWidgetByName(self, widget_name):
        return self.binds.findChild(QWidget, widget_name)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # SELECT BIND WITH WHATEVER MOUSE BUTTON #
            key = int(str(watched.objectName()).split("_")[-1])
            if key != self.selectedBind:
                lastSelectedWidget = self.getWidgetByName(f"BindWidget_{self.selectedBind}")
                widget = self.getWidgetByName(watched.objectName())

                if lastSelectedWidget:
                    lastSelectedWidget.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                        f"border-radius: 5px;")
                    keybind = lastSelectedWidget.findChild(QLabel, "Keybind")
                    action = lastSelectedWidget.findChild(QLabel, "Action")
                    if keybind:
                        keybind.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")
                    if action:
                        action.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")

                if widget:
                    widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};"
                                         f"border-radius: 5px;")
                    keybind = widget.findChild(QLabel, "Keybind")
                    action = widget.findChild(QLabel, "Action")
                    if keybind:
                        keybind.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                            f"color: #ffffff; font-weight: 500;")
                    if action:
                        action.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                            f"color: #ffffff; font-weight: 700;")

                self.removeButton.setDisabled(False)
                self.selectedBind = key

            else:
                # DESELECT BIND #
                widget = self.getWidgetByName(watched.objectName())
                widget.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                    f"border-radius: 5px;")
                keybind = widget.findChild(QLabel, "Keybind")
                action = widget.findChild(QLabel, "Action")
                if keybind:
                    keybind.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                        f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")
                if action:
                    action.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                        f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")

                self.removeButton.setDisabled(True)
                self.selectedBind = None

        return super().eventFilter(watched, event)

    def apply_button_styles(self, button):
        button.setStyleSheet(f"""
            QPushButton {{
                background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
                font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};
                font-weight: 500;
                border-radius: 5px;
                border: none;
                padding: 0 10px;
            }}

            QPushButton:hover {{
                background: {self.config.colorMode[self.config.selectedTheme]['hoverWidget']};
                color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
            }}

            QPushButton:pressed {{
                background: {self.config.colorMode[self.config.selectedTheme]['pressedWidget']};
                color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
            }}
        """)
