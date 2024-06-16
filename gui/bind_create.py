import math

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QKeySequenceEdit, QLineEdit, QFrame, QScrollArea, \
    QPushButton

from backend.config import Config


class BindCreate(QWidget):
    switchTab = pyqtSignal(int)
    bindCreate = pyqtSignal()

    def __init__(self, actions, binds):
        super().__init__()

        self.config = Config()

        self.actions = actions
        self.binds = binds

        self.buttonHeight = int(32 * self.config.scale[self.config.selectedScale]['scale'])

        self.selectedAction = None

        self.combination_found = False

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # layout.setContentsMargins(10, 0, 8, 0)

        bottomMargin = 0

        if self.config.selectedScale == 1:
            bottomMargin = 6
        elif self.config.selectedScale == 2:
            bottomMargin = 8
        elif self.config.selectedScale == 3:
            bottomMargin = 10
        elif self.config.selectedScale == 4:
            bottomMargin = 12
        else:
            bottomMargin = 0

        layout.setContentsMargins(8, 0, 8, bottomMargin)

        # ACTION LIST #

        self.actionsList = QWidget()
        self.actionsLayout = QVBoxLayout(self.actionsList)
        self.actionsLayout.setContentsMargins(5, 0, 5, 0)
        self.actionsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.actionsLayout.setSpacing(5)

        header = QLabel("Add bind:")
        header.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        header.setContentsMargins(1, 0, 0, 0)

        self.keybindHeader = QLabel("Key bind:")
        self.keybindHeader.setContentsMargins(1, 0, 0, 0)
        self.keybindHeader.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")

        keybindWidget = QWidget()
        keybindWidget.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
        keybindWidget.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
            f"border-radius: 5px; margin: 0 5px 0 5px;")
        keybindLayout = QHBoxLayout(keybindWidget)

        self.key_sequence_edit = QKeySequenceEdit()
        self.key_sequence_edit.setMaximumSequenceLength(1)
        self.key_sequence_edit.setClearButtonEnabled(True)
        self.key_sequence_edit.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
        self.key_sequence_edit.editingFinished.connect(self.handle_key_sequence)
        keybind_lineedit = self.key_sequence_edit.findChild(QLineEdit)
        keybind_lineedit.setCursor(Qt.CursorShape.PointingHandCursor)
        keybind_lineedit.textChanged.connect(self.set_uppercase_and_center_text)

        keybindLayout.addWidget(self.key_sequence_edit)

        actionHeader = QLabel("Actions:")
        actionHeader.setContentsMargins(1, 0, 0, 0)
        actionHeader.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 500;")

        for key, action_info in self.actions.actions.items():
            action_name = list(self.actions.actions[key].keys())[0]
            if key == 4:
                # LINE (SEPARATOR) #

                line = QFrame()
                line.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
                line.setFixedHeight(2)
                line.setFrameShadow(QFrame.Shadow.Plain)

                lineLayout = QVBoxLayout()
                lineLayout.addWidget(line)
                lineLayout.setContentsMargins(0, 2, 0, 2)

                self.actionsLayout.addLayout(lineLayout)
                continue

            action_widget = QWidget()
            action_widget.setObjectName(f"BindAction_{key}")
            action_widget.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
            action_layout = QHBoxLayout(action_widget)
            action_widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                f"border-radius: 5px;")

            actionLabel = QLabel(action_name)
            actionLabel.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
            actionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

            action_layout.addWidget(actionLabel)

            action_widget.installEventFilter(self)

            self.actionsLayout.addWidget(action_widget)

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
        scroll_area.setWidget(self.actionsList)

        # BUTTONS #

        buttons = QWidget()
        buttonsLayout = QVBoxLayout(buttons)

        createButton = QPushButton("Create")
        createButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(createButton, '#3498DB', '#2980b9', '#206694')

        cancelButton = QPushButton("Cancel")
        cancelButton.setFixedHeight(self.buttonHeight)
        self.apply_button_styles(cancelButton, '#EB4D4B', '#D34543', '#A83735')

        buttonsLayout.addWidget(createButton)
        buttonsLayout.addWidget(cancelButton)

        createButton.clicked.connect(self.createBind)
        cancelButton.clicked.connect(lambda: self.switchTab.emit(5))

        buttonsLayout.setContentsMargins(5, 0, 11, 8)

        # SETUP EVERYTHING #

        layout.addWidget(header)
        layout.addWidget(self.keybindHeader)
        layout.addWidget(keybindWidget)
        layout.addWidget(actionHeader)
        layout.addWidget(scroll_area)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def createBind(self):
        key_sequence = self.key_sequence_edit.keySequence().toString().upper()
        key_sequence = " + ".join(key_sequence.split("+"))
        if self.selectedAction is not None and not self.combination_found and not key_sequence == "":
            widget = self.getWidgetByName(f"BindAction_{self.selectedAction}")
            label = widget.findChild(QLabel)
            widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                                 f"border-radius: 5px;")
            label.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
            self.binds.push(key_sequence, label.text())
            self.selectedAction = None
            self.bindCreate.emit()
            self.switchTab.emit(5)

    def getWidgetByName(self, widget_name):
        return self.actionsList.findChild(QWidget, widget_name)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # SELECT ACTION WITH WHATEVER MOUSE BUTTON #
            key = int(str(watched.objectName()).split("_")[-1])
            if key != self.selectedAction:
                lastSelectedWidget = self.getWidgetByName(f"BindAction_{self.selectedAction}")
                widget = self.getWidgetByName(watched.objectName())

                if lastSelectedWidget:
                    lastSelectedWidget.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                        f"border-radius: 5px;")
                    label = lastSelectedWidget.findChild(QLabel)
                    if label:
                        label.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")

                if widget:
                    widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};"
                                         f"border-radius: 5px;")
                    label = widget.findChild(QLabel)
                    if label:
                        label.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                            f"color: #ffffff; font-weight: 700;")

                self.selectedAction = key

        return super().eventFilter(watched, event)

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

    def handle_key_sequence(self):
        if self.key_sequence_edit.hasFocus():
            key_sequence = self.key_sequence_edit.keySequence().toString().upper()
            key_sequence = " + ".join(key_sequence.split("+"))

            self.combination_found = False

            for combination, action_info in self.binds.get().items():
                for sequence, action in action_info.items():
                    if sequence == key_sequence:
                        self.keybindHeader.setText("Key bind: <font color='#EB4D4B'>(This combination exists!)</font>")
                        self.combination_found = True
                        break
            else:
                self.keybindHeader.setText("Key bind:")

    def set_uppercase_and_center_text(self):
        line_edit = self.key_sequence_edit.findChild(QLineEdit, "qt_keysequenceedit_lineedit")
        if line_edit:
            line_edit.blockSignals(True)
            text = line_edit.text().upper().replace('+', ' + ')
            line_edit.setText(text)
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            line_edit.blockSignals(False)

    def clear_sequence(self):
        self.key_sequence_edit.clear()
        lastSelectedWidget = self.getWidgetByName(f"BindAction_{self.selectedAction}")
        if lastSelectedWidget:
            lastSelectedWidget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                f"border-radius: 5px;")
            label = lastSelectedWidget.findChild(QLabel)
            if label:
                label.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                    f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 700;")
        self.selectedAction = None
        self.keybindHeader.setText("Key bind:")
        line_edit = self.key_sequence_edit.findChild(QLineEdit, "qt_keysequenceedit_lineedit")
        if line_edit:
            line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
