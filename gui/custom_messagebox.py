from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, \
    QSpacerItem

from backend.config import Config
from gui.custom_titlebar import CustomTitleBar
from gui.svg_color_widget import SVGColorWidget


def apply_button_styles(button, base_color, hover_color, pressed_color, font_size):
    button.setStyleSheet(f"""
        QPushButton {{
            background: {base_color};
            color: #ffffff;
            font-size: {font_size};
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


class CustomMessageBox(QMainWindow):
    def __init__(self, mode, message, buttons):
        super().__init__()
        self.config = Config()
        self.mode = 'SOUNDSYNC'
        match mode:
            case 0:
                self.mode = 'Info'
            case 1:
                self.mode = 'Warning'
            case 2:
                self.mode = 'Error'

        self.message = message
        self.buttons = buttons

        self.scale = self.config.scale
        self.scaleTitlebar = self.config.scaleTitlebar
        self.selectedScale = self.config.selectedScale
        self.colorMode = self.config.colorMode
        self.selectedTheme = self.config.selectedTheme
        self.scaleMessageBox = self.config.scaleMessageBox

        if self.scaleMessageBox:
            self.buttonWidth = int(130 * self.scale[self.selectedScale]['scale'])
            self.buttonHeight = int(32 * self.scale[self.selectedScale]['scale'])
            self.iconSize = int(60 * self.scale[self.selectedScale]['scale'])
            self.labelFontSize = self.scale[self.selectedScale]['font-size-smaller']
            self.buttonFontSize = self.scale[self.selectedScale]['font-size-smaller']
        else:
            self.buttonWidth = 130
            self.buttonHeight = 32
            self.iconSize = 60
            self.labelFontSize = '14px'
            self.buttonFontSize = '14px'
            if self.scaleTitlebar:
                self.scaleTitlebar = False

        self.setStyleSheet(
            f"QMainWindow {{background: {self.colorMode[self.selectedTheme]['windowBackground']}; border: 1px solid {self.colorMode[self.selectedTheme]['lineColor']}; }}")

        self.initUI()

    def initUI(self):
        main = QWidget(self)
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main.setStyleSheet("font-family: 'Poppins';")

        self.setCentralWidget(main)

        title_bar = CustomTitleBar(self, False, False, self.mode.upper())
        if self.scaleMessageBox:
            self.setFixedSize(int(300 * self.scale[self.selectedScale]['scale']), int(172 * self.scale[self.selectedScale]['scale']))
        else:
            self.setFixedSize(300, 172)

        self.center()

        self.setWindowTitle('SoundSync')
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        info = QWidget()
        info_layout = QHBoxLayout(info)
        info_layout.setContentsMargins(16, 8, 16, 8)

        match self.mode:
            case "Info":
                icon = SVGColorWidget(':/info_box.svg', self.iconSize, self.iconSize, "#2196F3")
            case "Warning":
                icon = SVGColorWidget(':/warning.svg', self.iconSize, self.iconSize, "#F0932B")
            case "Error":
                icon = SVGColorWidget(':/error.svg', self.iconSize, self.iconSize, "#EB4D4B")
            case _:
                icon = SVGColorWidget(':/info_box.svg', self.iconSize, self.iconSize, "#EB4D4B")

        label = QLabel(self.message)
        label.setWordWrap(True)
        label.setStyleSheet(
            f"font-weight: 500; font-size: {self.labelFontSize}; color: {self.colorMode[self.selectedTheme]['text-color']}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(icon)
        info_layout.addWidget(label)

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        if self.scaleMessageBox:
            buttons.setFixedHeight(int(52 * self.scale[self.selectedScale]['scale']))
        else:
            buttons.setFixedHeight(52)

        buttons.setStyleSheet(f"background: {self.colorMode[self.selectedTheme]['widgetBackground']};")
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(15, 0, 15, 0)

        colors = {'blue': ('#3498DB', '#2980b9', '#206694'),
                  'red': ('#EB4D4B', '#D34543', '#A83735'),
                  'default': ('#3498DB', '#2980b9', '#206694')}

        count_buttons = len(self.buttons)

        for button in self.buttons:
            name, color, action = button
            actionButton = QPushButton(name)
            actionButton.setFixedHeight(self.buttonHeight)

            color_styles = colors.get(color, colors['default'])
            apply_button_styles(actionButton, *color_styles, self.buttonFontSize)

            if action:
                actionButton.clicked.connect(lambda checked, click_action=action: self.handle_button_click(click_action))
            else:
                actionButton.clicked.connect(self.handle_None_button)

            if count_buttons == 2:
                buttons_layout.addWidget(actionButton)
                buttons_layout.setStretchFactor(actionButton, 1)
            else:
                spacer_left = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                buttons_layout.addSpacerItem(spacer_left)
                actionButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                buttons_layout.addWidget(actionButton)

        main_layout.addWidget(title_bar)
        main_layout.addWidget(info)
        main_layout.addWidget(buttons)

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handle_button_click(self, action):
        if callable(action):
            action()
        self.close()

    def handle_None_button(self):
        self.close()
