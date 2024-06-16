from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from backend.config import Config


class BindRemove(QWidget):
    switchTab = pyqtSignal(int)
    confirmRemoveBind = pyqtSignal()

    def __init__(self, actions, binds):
        super().__init__()

        self.config = Config()
        self.binds = binds

        self.buttonHeight = int(32 * self.config.scale[self.config.selectedScale]['scale'])
        self.labelHeight = int(30 * self.config.scale[self.config.selectedScale]['scale'])
        self.widgetHeight = int(36 * self.config.scale[self.config.selectedScale]['scale'])

        self.actions = actions

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 8, 0)

        dialog = QWidget()
        dialogLayout = QVBoxLayout(dialog)

        header = QLabel("Are you sure?")
        header.setFixedHeight(self.labelHeight)
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-dialog-bigger']};"
            f"font-weight: 600; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        header.setContentsMargins(0, 0, 0, 0)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info = QLabel("You want do delete this bind?")
        info.setFixedHeight(self.labelHeight)
        info.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-dialog-smaller']};"
            f"font-weight: 400; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        info.setContentsMargins(0, 0, 0, 0)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # KEYBIND #

        keybindWidget = QWidget()
        keybindWidget.setFixedHeight(self.widgetHeight)
        keybindWidget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                                    f"border-radius: 5px;")
        keybindLayout = QHBoxLayout(keybindWidget)

        self.keybind = QLabel("")
        self.keybind.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
        self.keybind.setAlignment(Qt.AlignmentFlag.AlignCenter)

        keybindLayout.addWidget(self.keybind)

        # ACTION #

        actionWidget = QWidget()
        actionWidget.setFixedHeight(self.widgetHeight)
        actionWidget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                                   f"border-radius: 5px;")
        actionLayout = QHBoxLayout(actionWidget)

        self.action = QLabel("")
        self.action.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
        self.action.setAlignment(Qt.AlignmentFlag.AlignCenter)

        actionLayout.addWidget(self.action)

        # BUTTONS #

        buttons = QWidget()
        buttonsLayout = QVBoxLayout(buttons)

        acceptButton = QPushButton("Accept")
        acceptButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(acceptButton, '#3498DB', '#2980b9', '#206694')

        cancelButton = QPushButton("Cancel")
        cancelButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(cancelButton, '#EB4D4B', '#D34543', '#A83735')

        buttonsLayout.addWidget(acceptButton)
        buttonsLayout.addWidget(cancelButton)

        acceptButton.clicked.connect(self.confirmRemoveBind.emit)
        cancelButton.clicked.connect(lambda: self.switchTab.emit(5))

        buttonsLayout.setContentsMargins(0, 10, 0, 0)

        buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # SETUP EVERYTHING #

        dialogLayout.addWidget(header)
        dialogLayout.addWidget(info)
        dialogLayout.addWidget(keybindWidget)
        dialogLayout.addWidget(actionWidget)
        dialogLayout.addWidget(buttons)

        layout.addWidget(dialog)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(layout)

    def get_combination_and_action(self, key):
        inner_dict = self.binds.get()[key]
        if inner_dict:
            for combination, action in inner_dict.items():
                return combination, action
        return None, None

    def showKeybind(self, index):
        combination, action = self.get_combination_and_action(index)
        self.keybind.setText(combination)
        self.action.setText(action)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def apply_button_styles(self, button, base_color, hover_color, pressed_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background: {base_color};
                color: #ffffff;
                font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};
                font-weight: 600;
                border-radius: 5px;
                border: none;
            }}

            QPushButton:hover {{
                background: {hover_color};
                color: #ffffff;
            }}

            QPushButton:pressed {{
                background: {pressed_color};
                color: #ffffff;
            }}
        """)