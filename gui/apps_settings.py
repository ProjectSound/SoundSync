import math

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QPushButton

from backend.config import Config
from gui.svg_color_widget import SVGColorWidget


class AppsSettings(QWidget):
    switchTab = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.config = Config()

        self.iconSize = int(28 * self.config.scale[self.config.selectedScale]['scale'])
        self.infoWidgetSize = int(120 * self.config.scale[self.config.selectedScale]['scale'])
        self.labelHeight = int(24 * self.config.scale[self.config.selectedScale]['scale'])
        self.statusHeight = int(34 * self.config.scale[self.config.selectedScale]['scale'])
        self.buttonHeight = int(32 * self.config.scale[self.config.selectedScale]['scale'])

        self.sliderHeight = int(25 * self.config.scale[self.config.selectedScale]['scale'])
        self.sliderSize = int(6 * self.config.scale[self.config.selectedScale]['scale'])
        self.sliderBorderRadius = math.floor(self.sliderSize / 2)
        self.addToWidth = 0
        if self.config.selectedScale == 2:
            self.addToWidth = 1
        else:
            self.addToWidth = 0

        self.sliderHandleWidth = int(20 * self.config.scale[self.config.selectedScale]['scale'] + self.addToWidth)
        self.sliderHandleBorderRadius = int(10 * self.config.scale[self.config.selectedScale]['scale'])
        self.addToSize = 0
        if self.config.selectedScale == 1 or self.config.selectedScale == 2:
            self.addToSize = 1
        else:
            self.addToSize = 0

        self.sliderMargin = math.floor(int(7 * self.config.scale[self.config.selectedScale]['scale']) + self.addToSize)

        self.cantExceedNormal = 0
        self.cantExceedLow = 0

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        info = QWidget()
        infoLayout = QHBoxLayout(info)

        # NORMAL VOLUME #

        normalVolumeWidget = QWidget()
        normalVolumeWidget.setFixedSize(self.infoWidgetSize, self.infoWidgetSize)
        normalVolumeWidget.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        normalVolumeLayout = QVBoxLayout(normalVolumeWidget)
        normalVolumeLayout.setContentsMargins(0, 0, 0, 0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerLayout.setSpacing(0)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/input.svg', self.iconSize, self.iconSize,
                              self.config.colorMode[self.config.selectedTheme]['text-color'])
        icon.setFixedSize(self.iconSize, self.iconSize)

        label = QLabel("Normal sound level")
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};"
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)

        self.procentNormalLabel = QLabel()
        self.procentNormalLabel.setContentsMargins(0, 0, 0, 5)
        self.procentNormalLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.procentNormalLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>100%</font>")
        self.procentNormalLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 700;")

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)
        iconContainerLayout.addWidget(self.procentNormalLabel)

        normalVolumeLayout.addWidget(iconContainerWidget)

        # REDUCED VOLUME #

        lowVolumeWidget = QWidget()
        lowVolumeWidget.setFixedSize(self.infoWidgetSize, self.infoWidgetSize)
        lowVolumeWidget.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        lowVolumeLayout = QVBoxLayout(lowVolumeWidget)
        lowVolumeLayout.setContentsMargins(0, 0, 0, 0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerLayout.setSpacing(0)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/low_volume.svg', self.iconSize, self.iconSize,
                              self.config.colorMode[self.config.selectedTheme]['text-color'])
        icon.setFixedSize(self.iconSize, self.iconSize)

        label = QLabel("Turned down to level")
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};"
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)

        self.procentLowLabel = QLabel()
        self.procentLowLabel.setContentsMargins(0, 0, 0, 5)
        self.procentLowLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.procentLowLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>20%</font>")
        self.procentLowLabel.setStyleSheet(f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
                                           f"font-weight: 700;")

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)
        iconContainerLayout.addWidget(self.procentLowLabel)

        lowVolumeLayout.addWidget(iconContainerWidget)

        # LINE (SEPARATOR) #

        line = QFrame()
        line.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line.setFixedSize(int(275 * self.config.scale[self.config.selectedScale]['scale']), 1)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # SETTINGS LIST #

        settings = QWidget()
        # settings.setFixedWidth(int(307 * scale[selectedScale]['scale']))
        settingsLayout = QVBoxLayout(settings)
        settingsLayout.setContentsMargins(0, 0, 0, 0)

        # NORMAL SOUND LEVEL #

        normal = QWidget()
        normalLayout = QVBoxLayout(normal)
        normalLayout.setContentsMargins(5, 0, 5, 5)

        label = QLabel("Normal sound level:")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.normalSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.normalSlider.setFixedHeight(self.sliderHeight)
        self.normalSlider.setMinimum(1)
        self.normalSlider.setMaximum(100)
        self.normalSlider.setValue(100)
        self.normalSlider.valueChanged.connect(lambda value, name="Normal": self.handleSliderValue(value, name))
        self.normalSlider.setStyleSheet(f"""
                    QSlider::groove:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['sliderBackground']};
                        height: {self.sliderSize}px;
                        border-radius: {self.sliderBorderRadius}px;
                    }}

                    QSlider::handle:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                        width: {self.sliderHandleWidth}px;
                        margin: -{self.sliderMargin}px 0;
                        border-radius: {self.sliderHandleBorderRadius}px;
                    }}
                    QSlider::sub-page:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                        border-radius: {self.sliderBorderRadius}px;
                    }}
                """)

        procent = QWidget()
        procent.setFixedHeight(self.statusHeight)
        procent.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                              f"border-radius: 5px;")
        procentLayout = QHBoxLayout(procent)

        self.procentLabelNormal = QLabel("100%")
        self.procentLabelNormal.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.procentLabelNormal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        procentLayout.addWidget(self.procentLabelNormal)

        normalLayout.addWidget(label)
        normalLayout.addWidget(self.normalSlider)
        normalLayout.addWidget(procent)

        settingsLayout.addWidget(normal)

        # REDUCED SOUND LEVEL #

        reduced = QWidget()
        reducedLayout = QVBoxLayout(reduced)
        reducedLayout.setContentsMargins(5, 0, 5, 5)

        label = QLabel("Turned down to level:")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.lowSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.lowSlider.setFixedHeight(self.sliderHeight)
        self.lowSlider.setMinimum(1)
        self.lowSlider.setMaximum(100)
        self.lowSlider.setValue(20)
        self.lowSlider.valueChanged.connect(lambda value, name="Reduced": self.handleSliderValue(value, name))
        self.lowSlider.setStyleSheet(f"""
                    QSlider::groove:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['sliderBackground']};
                        height: {self.sliderSize}px;
                        border-radius: {self.sliderBorderRadius}px;
                    }}

                    QSlider::handle:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                        width: {self.sliderHandleWidth}px;
                        margin: -{self.sliderMargin}px 0px;
                        border-radius: {self.sliderHandleBorderRadius}px;
                    }}
                    QSlider::sub-page:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};
                        border-radius: {self.sliderBorderRadius}px;
                    }}
                """)

        procent = QWidget()
        procent.setFixedHeight(self.statusHeight)
        procent.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                              f"border-radius: 5px;")
        procentLayout = QHBoxLayout(procent)

        self.procentLabelLow = QLabel("20%")
        self.procentLabelLow.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700;"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.procentLabelLow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        procentLayout.addWidget(self.procentLabelLow)

        reducedLayout.addWidget(label)
        reducedLayout.addWidget(self.lowSlider)
        reducedLayout.addWidget(procent)

        settingsLayout.addWidget(reduced)

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

        buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        buttonsLayout.setContentsMargins(5, 0, 5, 8)
        buttonsLayout.setSpacing(5)

        acceptButton.clicked.connect(self.saveSettings)
        cancelButton.clicked.connect(self.cancelChanges)

        # COMBINE EVERYTHING #

        infoLayout.addWidget(normalVolumeWidget)
        infoLayout.addWidget(lowVolumeWidget)

        layout.addWidget(info)
        layout.addWidget(line, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(settings)
        layout.addWidget(buttons)

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

        self.changeSlidersPosition()

        self.setLayout(layout)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def displaySettings(self):
        self.procentNormalLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.normal_sound_level}%</font>")
        self.procentLowLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.reduced_sound_level}%</font>")

    def saveSettings(self):
        self.config.normal_sound_level = self.normalSlider.value()
        self.config.reduced_sound_level = self.lowSlider.value()
        self.config.save()
        self.switchTab.emit(2)

    def cancelChanges(self):
        self.switchTab.emit(2)
        self.changeSlidersPosition()

    def handleSliderValue(self, value, name):
        normalVolume = self.normalSlider.value()
        lowVolume = self.lowSlider.value()

        if name == "Normal":
            if normalVolume > lowVolume:
                if not value == 0:
                    self.cantExceedNormal = value
                self.normalSlider.setValue(value)
                self.updateValue(value, name)
            else:
                self.normalSlider.setSliderPosition(self.cantExceedNormal)
        elif name == "Reduced":
            if normalVolume > lowVolume:
                if not value == 0:
                    self.cantExceedLow = value
                self.lowSlider.setValue(value)
                self.updateValue(value, name)
            else:
                self.lowSlider.setSliderPosition(self.cantExceedLow)

    def changeSlidersPosition(self):
        self.normalSlider.setSliderPosition(self.config.normal_sound_level)
        self.lowSlider.setSliderPosition(self.config.reduced_sound_level)

    def updateValue(self, value, name):
        if name == "Normal":
            self.procentLabelNormal.setText(f"{value}%")
        elif name == "Reduced":
            self.procentLabelLow.setText(f"{value}%")

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
