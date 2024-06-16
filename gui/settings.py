import os
import sys

from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton, QComboBox

from backend.config import Config

import version


class Settings(QWidget):
    def __init__(self, settings_core):
        super().__init__()

        self.config = Config()

        self.settings_core = settings_core

        self.statusWidth = int(60 * self.config.scale[self.config.selectedScale]['scale'])
        self.statusHeight = int(30 * self.config.scale[self.config.selectedScale]['scale'])
        self.labelHeight = int(30 * self.config.scale[self.config.selectedScale]['scale'])
        self.comboboxWidth = int(90 * self.config.scale[self.config.selectedScale]['scale'])
        self.lineWidth = int(290 * self.config.scale[self.config.selectedScale]['scale'])

        self.comboboxArrowSize = int(12 * self.config.scale[self.config.selectedScale]['scale'])
        self.comboboxArrowMargin = self.comboboxArrowSize + int(3 * self.config.scale[self.config.selectedScale]['scale'])

        self.newScale = self.config.selectedScale
        self.newTheme = self.config.selectedTheme
        self.newScaleTitlebar = self.config.scaleTitlebar
        self.newScaleMessageBox = self.config.scaleMessageBox

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # layout.setContentsMargins(12, 0, 8, 0)

        bottomMargin = 4

        if self.config.selectedScale == 1:
            bottomMargin = 9
        elif self.config.selectedScale == 2:
            bottomMargin = 10
        elif self.config.selectedScale == 3:
            bottomMargin = 11
        elif self.config.selectedScale == 4:
            bottomMargin = 12
        else:
            bottomMargin = 4

        layout.setContentsMargins(8, 0, 8, bottomMargin)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 0, 5, 0)

        header = QLabel("Settings:")
        header.setFixedHeight(self.labelHeight)
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        header.setContentsMargins(0, 0, 0, 0)

        # LINE (SEPARATOR) #

        line = QFrame()
        line.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line.setFixedSize(self.lineWidth, 1)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # AUTO LAUNCH #

        launch = QWidget()
        launchLayout = QHBoxLayout(launch)

        label = QLabel("Auto launch on windows startup")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.launchStatus = QPushButton()
        self.launchStatus.setFixedSize(self.statusWidth, self.statusHeight)
        if self.config.auto_launch:
            self.launchStatus.setText("ON")
            self.launchStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        else:
            self.launchStatus.setText("OFF")
            self.launchStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")

        launchLayout.addWidget(label)
        launchLayout.addWidget(self.launchStatus)
        launchLayout.setContentsMargins(0, 0, 0, 0)

        self.launchStatus.clicked.connect(self.toggleAutoLaunch)

        # MINIMIZE TO TRAY #

        tray = QWidget()
        trayLayout = QHBoxLayout(tray)

        label = QLabel("Minimize to app tray when closing")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.trayStatus = QPushButton()
        self.trayStatus.setFixedSize(self.statusWidth, self.statusHeight)
        if self.config.minimize_to_tray:
            self.trayStatus.setText("ON")
            self.trayStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
        else:
            self.trayStatus.setText("OFF")
            self.trayStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")

        trayLayout.addWidget(label)
        trayLayout.addWidget(self.trayStatus)
        trayLayout.setContentsMargins(0, 0, 0, 0)

        self.trayStatus.clicked.connect(self.toggleMinimizeToTray)

        # LINE 2 (SEPARATOR) #

        line2 = QFrame()
        line2.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line2.setFixedSize(self.lineWidth, 1)
        line2.setFrameShadow(QFrame.Shadow.Plain)

        # SCALE TITLEBAR #

        scalableTitlebar = QWidget()
        scalableTitlebarLayout = QHBoxLayout(scalableTitlebar)

        label = QLabel("Scale titlebar")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.scaleTitlebarStatus = QPushButton()
        self.scaleTitlebarStatus.setFixedSize(self.statusWidth, self.statusHeight)

        if self.config.scaleTitlebar:
            self.scaleTitlebarStatus.setText("ON")
            self.scaleTitlebarStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
        else:
            self.scaleTitlebarStatus.setText("OFF")
            self.scaleTitlebarStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")

        scalableTitlebarLayout.addWidget(label)
        scalableTitlebarLayout.addWidget(self.scaleTitlebarStatus)
        scalableTitlebarLayout.setContentsMargins(0, 0, 0, 0)

        self.scaleTitlebarStatus.clicked.connect(self.toggleScaleTitlebar)

        # SCALE MESSAGEBOX #

        scalableMessageBox = QWidget()
        scalableMessageBoxLayout = QHBoxLayout(scalableMessageBox)

        label = QLabel("Scale message box")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.scalableMessageBoxStatus = QPushButton()
        self.scalableMessageBoxStatus.setFixedSize(self.statusWidth, self.statusHeight)

        if self.config.scaleMessageBox:
            self.scalableMessageBoxStatus.setText("ON")
            self.scalableMessageBoxStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
        else:
            self.scalableMessageBoxStatus.setText("OFF")
            self.scalableMessageBoxStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")

        scalableMessageBoxLayout.addWidget(label)
        scalableMessageBoxLayout.addWidget(self.scalableMessageBoxStatus)
        scalableMessageBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.scalableMessageBoxStatus.clicked.connect(self.toggleScaleMessageBox)

        # LINE 3 (SEPARATOR) #

        line3 = QFrame()
        line3.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line3.setFixedSize(self.lineWidth, 1)
        line3.setFrameShadow(QFrame.Shadow.Plain)

        # SCALE #

        scaleWidget = QWidget()
        scaleLayout = QHBoxLayout(scaleWidget)

        label = QLabel("Scale")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.scaleComboBox = QComboBox()
        self.scaleComboBoxIcon = "url(:/arrow_down.svg)" if self.config.selectedTheme == 0 else "url(:/arrow_down_dark.svg)"
        self.scaleComboBox.setFixedSize(self.comboboxWidth, self.labelHeight)
        self.scaleComboBox.setStyleSheet(f"""
            QComboBox{{
                border: none;
                background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
                border-radius: 4px;
                padding-left: 10px;
                font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};
                font-weight: 600;
                text-align: center;
            }}
            QComboBox::drop-down{{
                border: 0px;
            }}
            QComboBox::down-arrow{{
                image: {self.scaleComboBoxIcon};
                width: {self.comboboxArrowSize}px;
                height: {self.comboboxArrowSize}px;
                margin-right: {self.comboboxArrowMargin}px;
            }}
            QComboBox QListView{{
                font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};
                border: 1px solid rgba(0, 0, 0, 10%);
                padding: 5px;
                background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                outline: 0px;
            }}
            QComboBox QListView:item{{
                padding-left: 10px;
                background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
            }}
            QComboBox QListView:item:hover{{
                background-color: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
            }}
            QComboBox QListView:item:selected {{
                color: #fff;
                background-color: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
            }}
        """)
        self.scaleComboBox.addItem('100%')
        self.scaleComboBox.addItem('125%')
        self.scaleComboBox.addItem('150%')
        self.scaleComboBox.addItem('175%')
        self.scaleComboBox.addItem('200%')

        self.scaleComboBox.setCurrentIndex(self.config.selectedScale)

        self.scaleComboBox.currentIndexChanged.connect(self.currentIndexChanged)

        scaleLayout.addWidget(label)
        scaleLayout.addWidget(self.scaleComboBox)

        scaleLayout.setContentsMargins(0, 4, 0, 4)

        # THEME #

        theme = QWidget()
        themeLayout = QHBoxLayout(theme)

        label = QLabel("Theme")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.themeComboBox = QComboBox()
        self.themeComboBoxIcon = "url(:/arrow_down.svg)" if self.config.selectedTheme == 0 else "url(:/arrow_down_dark.svg)"
        self.themeComboBox.setFixedSize(self.comboboxWidth, self.labelHeight)
        self.themeComboBox.setStyleSheet(f"""
                    QComboBox{{
                        border: none;
                        background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                        color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
                        border-radius: 4px;
                        padding-left: 10px;
                        font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};
                        font-weight: 600;
                        text-align: center;
                    }}
                    QComboBox::drop-down{{
                        border: 0px;
                    }}
                    QComboBox::down-arrow{{
                        image: {self.themeComboBoxIcon};
                        width: {self.comboboxArrowSize}px;
                        height: {self.comboboxArrowSize}px;
                        margin-right: {self.comboboxArrowMargin}px;
                    }}
                    QComboBox QListView{{
                        font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};
                        border: 1px solid rgba(0, 0, 0, 10%);
                        padding: 5px;
                        background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                        outline: 0px;
                    }}
                    QComboBox QListView:item{{
                        padding-left: 10px;
                        background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                        color: {self.config.colorMode[self.config.selectedTheme]['text-color']};
                    }}
                    QComboBox QListView:item:hover{{
                        background-color: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                    }}
                    QComboBox QListView:item:selected {{
                        color: #fff;
                        background-color: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                    }}
                """)
        self.themeComboBox.addItem('LIGHT')
        self.themeComboBox.addItem('DARK')

        self.themeComboBox.setCurrentIndex(self.config.selectedTheme)

        self.themeComboBox.currentIndexChanged.connect(self.currentIndexChanged)

        themeLayout.addWidget(label)
        themeLayout.addWidget(self.themeComboBox)

        themeLayout.setContentsMargins(0, 4, 0, 4)

        # LINE 4 (SEPARATOR) #

        line4 = QFrame()
        line4.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line4.setFixedSize(self.lineWidth, 1)
        line4.setFrameShadow(QFrame.Shadow.Plain)

        # RESTART BUTTON #

        self.restart = QPushButton("Restart required for changes")
        self.restart.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
        self.apply_button_styles(self.restart, '#EB4D4B', '#D34543', '#A83735')
        self.restart.clicked.connect(self.restartApp)
        self.restart.setVisible(False)

        # FOOTER #

        footer = QLabel(f"VERSION: {version.__version__}")
        footer.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['footerColor']};")
        footer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        footer.setContentsMargins(0, 0, 0, 0)

        # SETUP EVERYTHING #

        main_layout.addWidget(header)
        main_layout.addWidget(line, 0, Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(launch)
        main_layout.addWidget(tray)
        main_layout.addWidget(line2, 0, Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(scalableTitlebar)
        main_layout.addWidget(scalableMessageBox)
        main_layout.addWidget(line3, 0, Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(scaleWidget)
        main_layout.addWidget(theme)
        main_layout.addWidget(line4, 0, Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(self.restart)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(main_layout)

        layout.addWidget(footer)

        self.setLayout(layout)

    def currentIndexChanged(self, index):
        sender = self.sender()
        if sender == self.scaleComboBox:
            self.newScale = sender.currentIndex()
        elif sender == self.themeComboBox:
            self.newTheme = sender.currentIndex()

        self.checkIfRestartNeeded()

    def toggleAutoLaunch(self, event):
        if self.config.auto_launch:
            self.settings_core.remove_from_startup()
            self.launchStatus.setText("OFF")
            self.launchStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        else:
            self.settings_core.add_to_startup()
            self.launchStatus.setText("ON")
            self.launchStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")

    def toggleMinimizeToTray(self, event):
        if self.config.minimize_to_tray:
            self.trayStatus.setText("OFF")
            self.trayStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        else:
            self.trayStatus.setText("ON")
            self.trayStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        self.config.minimize_to_tray = not self.config.minimize_to_tray
        self.config.save()

    def toggleScaleTitlebar(self, event):
        if self.newScaleTitlebar:
            self.scaleTitlebarStatus.setText("OFF")
            self.scaleTitlebarStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        else:
            self.scaleTitlebarStatus.setText("ON")
            self.scaleTitlebarStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")

        self.newScaleTitlebar = not self.newScaleTitlebar

        self.checkIfRestartNeeded()

    def toggleScaleMessageBox(self, event):
        if self.newScaleMessageBox:
            self.scalableMessageBoxStatus.setText("OFF")
            self.scalableMessageBoxStatus.setStyleSheet(
                f"background: #FF4757; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")
        else:
            self.scalableMessageBoxStatus.setText("ON")
            self.scalableMessageBoxStatus.setStyleSheet(
                f"background: #2ECC71; border-radius: 5px; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700; ")

        self.newScaleMessageBox = not self.newScaleMessageBox

        self.checkIfRestartNeeded()

    def checkIfRestartNeeded(self):
        if (self.config.scaleTitlebar != self.newScaleTitlebar or self.config.selectedScale != self.newScale or
                self.config.selectedTheme != self.newTheme or self.config.scaleMessageBox != self.newScaleMessageBox):
            self.restart.setVisible(True)
        else:
            self.restart.setVisible(False)

    def restartApp(self):
        self.config.scaleTitlebar = self.newScaleTitlebar
        self.config.selectedScale = self.newScale
        self.config.selectedTheme = self.newTheme
        self.config.scaleMessageBox = self.newScaleMessageBox
        self.config.save()
        sys.argv = [sys.executable]
        script_path = os.path.abspath("main.py")
        sys.argv.extend([script_path])
        QCoreApplication.instance().quit()
        os.execl(sys.executable, *sys.argv)

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