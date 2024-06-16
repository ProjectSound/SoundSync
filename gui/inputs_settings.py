import math

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QPushButton

from backend.config import Config


class InputsSettings(QWidget):
    switchTab = pyqtSignal(int)

    def __init__(self, input_manager):
        super().__init__()

        self.config = Config()

        self.input_manager = input_manager

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

        self.initUI()

    def initUI(self):
        settings = QWidget()
        settingsLayout = QVBoxLayout(settings)
        settingsLayout.setSpacing(0)
        # settingsLayout.setContentsMargins(0, 0, 0, 0)

        # THRESHOLD SETTING (FIRST INPUT) #

        threshold = QWidget()
        thresholdLayout = QVBoxLayout(threshold)
        thresholdLayout.setContentsMargins(5, 0, 5, 5)

        label = QLabel("Threshold:")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.thresholdSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.thresholdSlider.setFixedHeight(self.sliderHeight)
        self.thresholdSlider.setMinimum(1)
        self.thresholdSlider.setMaximum(100)
        self.thresholdSlider.setValue(50)
        self.thresholdSlider.valueChanged.connect(lambda value, name="Threshold": self.handleSliderValue(value, name))
        self.thresholdSlider.setStyleSheet(f"""
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
        procent.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
        procentLayout = QHBoxLayout(procent)

        self.procentLabelThreshold = QLabel("50%")
        self.procentLabelThreshold.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.procentLabelThreshold.setAlignment(Qt.AlignmentFlag.AlignCenter)

        procentLayout.addWidget(self.procentLabelThreshold)

        thresholdLayout.addWidget(label)
        thresholdLayout.addWidget(self.thresholdSlider)
        thresholdLayout.addWidget(procent)

        # THRESHOLD NOT REACHED (FIRST INPUT) #

        thresholdReach = QWidget()
        thresholdReachLayout = QVBoxLayout(thresholdReach)
        thresholdReachLayout.setContentsMargins(5, 0, 5, 5)

        labelThresholdReach = QLabel("Threshold no reached:")
        labelThresholdReach.setFixedHeight(self.labelHeight)
        labelThresholdReach.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.thresholdReachSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.thresholdReachSlider.setFixedHeight(self.sliderHeight)
        self.thresholdReachSlider.setMinimum(1)
        self.thresholdReachSlider.setMaximum(100)
        self.thresholdReachSlider.setValue(50)
        self.thresholdReachSlider.valueChanged.connect(
            lambda value, name="ThresholdReach": self.handleSliderValue(value, name))
        self.thresholdReachSlider.setStyleSheet(f"""
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

        duration = QWidget()
        duration.setFixedHeight(self.statusHeight)
        duration.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
        durationLayout = QHBoxLayout(duration)

        self.durationThresholdLabel = QLabel("2s")
        self.durationThresholdLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.durationThresholdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        durationLayout.addWidget(self.durationThresholdLabel)

        thresholdReachLayout.addWidget(labelThresholdReach)
        thresholdReachLayout.addWidget(self.thresholdReachSlider)
        thresholdReachLayout.addWidget(duration)

        # THRESHOLD SETTING (SECOND INPUT) #

        thresholdSecond = QWidget()
        thresholdSecondLayout = QVBoxLayout(thresholdSecond)
        thresholdSecondLayout.setContentsMargins(5, 0, 5, 5)

        label = QLabel("Threshold of second input:")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.thresholdSecondSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.thresholdSecondSlider.setFixedHeight(self.sliderHeight)
        self.thresholdSecondSlider.setMinimum(1)
        self.thresholdSecondSlider.setMaximum(100)
        self.thresholdSecondSlider.setValue(30)
        self.thresholdSecondSlider.valueChanged.connect(
            lambda value, name="ThresholdSecond": self.handleSliderValue(value, name))
        self.thresholdSecondSlider.setStyleSheet(f"""
                    QSlider::groove:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['sliderBackground']};
                        height: {self.sliderSize}px;
                        border-radius: {self.sliderBorderRadius}px;
                    }}

                    QSlider::handle:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']};
                        width: {self.sliderHandleWidth}px;
                        margin: -{self.sliderMargin}px 0px;
                        border-radius: {self.sliderHandleBorderRadius}px;
                    }}
                    QSlider::sub-page:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']};
                        border-radius: {self.sliderBorderRadius}px;
                    }}
                """)

        procent = QWidget()
        procent.setFixedHeight(self.statusHeight)
        procent.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
        procentLayout = QHBoxLayout(procent)

        self.procentSecondLabel = QLabel("30%")
        self.procentSecondLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.procentSecondLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        procentLayout.addWidget(self.procentSecondLabel)

        thresholdSecondLayout.addWidget(label)
        thresholdSecondLayout.addWidget(self.thresholdSecondSlider)
        thresholdSecondLayout.addWidget(procent)

        # THRESHOLD NOT REACHED (SECOND INPUT) #

        thresholdReachSecond = QWidget()
        thresholdReachSecondLayout = QVBoxLayout(thresholdReachSecond)
        thresholdReachSecondLayout.setContentsMargins(5, 0, 5, 5)

        label = QLabel("Threshold of second input:")
        label.setFixedHeight(self.labelHeight)
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.thresholdReachSecondSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.thresholdReachSecondSlider.setFixedHeight(self.sliderHeight)
        self.thresholdReachSecondSlider.setMinimum(1)
        self.thresholdReachSecondSlider.setMaximum(100)
        self.thresholdReachSecondSlider.setValue(20)
        self.thresholdReachSecondSlider.valueChanged.connect(
            lambda value, name="ThresholdReachSecond": self.handleSliderValue(value, name))
        self.thresholdReachSecondSlider.setStyleSheet(f"""
                    QSlider::groove:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['sliderBackground']};
                        height: {self.sliderSize}px;
                        border-radius: {self.sliderBorderRadius}px;
                    }}

                    QSlider::handle:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']};
                        width: {self.sliderHandleWidth}px;
                        margin: -{self.sliderMargin}px 0px;
                        border-radius: {self.sliderHandleBorderRadius}px;
                    }}
                    QSlider::sub-page:horizontal {{
                        background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']};
                        border-radius: {self.sliderBorderRadius}px;
                    }}
                """)

        duration = QWidget()
        duration.setFixedHeight(self.statusHeight)
        duration.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
        durationLayout = QHBoxLayout(duration)

        self.durationSecondLabel = QLabel("2s")
        self.durationSecondLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.durationSecondLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        durationLayout.addWidget(self.durationSecondLabel)

        thresholdReachSecondLayout.addWidget(label)
        thresholdReachSecondLayout.addWidget(self.thresholdReachSecondSlider)
        thresholdReachSecondLayout.addWidget(duration)

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

        buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignBottom)
        buttonsLayout.setContentsMargins(5, 0, 5, 8)
        buttonsLayout.setSpacing(5)

        acceptButton.clicked.connect(self.saveSettings)
        cancelButton.clicked.connect(self.cancelChanges)

        # SETUP EVERYTHING #

        settingsLayout.addWidget(threshold, 0)
        settingsLayout.addWidget(thresholdReach, 0)
        settingsLayout.addWidget(thresholdSecond, 0)
        settingsLayout.addWidget(thresholdReachSecond, 0)
        settingsLayout.addWidget(buttons, 0)

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

        settingsLayout.setContentsMargins(8, 0, 8, bottomMargin)

        self.changeSlidersPosition()

        self.setLayout(settingsLayout)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def saveSettings(self):
        self.config.threshold1 = self.thresholdSlider.value()
        self.config.threshold2 = self.thresholdSecondSlider.value()
        self.config.threshold_not_reached1 = self.calculate_duration(self.thresholdReachSlider.value())
        self.config.threshold_not_reached2 = self.calculate_duration(self.thresholdReachSecondSlider.value())
        self.input_manager.update()
        self.config.save()
        self.switchTab.emit(0)

    def cancelChanges(self):
        self.switchTab.emit(0)
        self.changeSlidersPosition()

    def handleSliderValue(self, value, name):
        self.updateValue(value, name)

    def changeSlidersPosition(self):
        self.thresholdSlider.setSliderPosition(self.config.threshold1)
        self.thresholdReachSlider.setSliderPosition(self.calculate_slider_position(self.config.threshold_not_reached1))
        self.durationThresholdLabel.setText(f"{self.config.threshold_not_reached1:.2f}s")
        self.thresholdSecondSlider.setSliderPosition(self.config.threshold2)
        self.thresholdReachSecondSlider.setSliderPosition(self.calculate_slider_position(self.config.threshold_not_reached2))
        self.durationSecondLabel.setText(f"{self.config.threshold_not_reached2:.2f}s")

    def calculate_slider_position(self, duration):
        if duration <= 1:
            value = 1 + (duration - 0.5) * (9 / 0.5)
        elif duration <= 2:
            value = 10 + (duration - 1) * (10 / 1)
        elif duration <= 3:
            value = 20 + (duration - 2) * (10 / 1)
        elif duration <= 4:
            value = 30 + (duration - 3) * (10 / 1)
        elif duration <= 5:
            value = 40 + (duration - 4) * (10 / 1)
        elif duration <= 6:
            value = 50 + (duration - 5) * (10 / 1)
        elif duration <= 7:
            value = 60 + (duration - 6) * (10 / 1)
        elif duration <= 8:
            value = 70 + (duration - 7) * (10 / 1)
        elif duration <= 9:
            value = 80 + (duration - 8) * (10 / 1)
        elif duration <= 10:
            value = 90 + (duration - 9) * (10 / 1)
        else:
            value = 100

        return int(value)

    def calculate_duration(self, value):
        if value <= 10:
            duration = 0.5 + (value - 1) * (0.5 / 9)
        elif value <= 20:
            duration = 1 + (value - 10) * (1 / 10)
        elif value <= 30:
            duration = 2 + (value - 20) * (1 / 10)
        elif value <= 40:
            duration = 3 + (value - 30) * (1 / 10)
        elif value <= 50:
            duration = 4 + (value - 40) * (1 / 10)
        elif value <= 60:
            duration = 5 + (value - 50) * (1 / 10)
        elif value <= 70:
            duration = 6 + (value - 60) * (1 / 10)
        elif value <= 80:
            duration = 7 + (value - 70) * (1 / 10)
        elif value <= 90:
            duration = 8 + (value - 80) * (1 / 10)
        elif value <= 100:
            duration = 9 + (value - 90) * (1 / 10)
        else:
            duration = 10

        return duration

    def updateValue(self, value, name):
        if name == "Threshold":
            self.procentLabelThreshold.setText(f"{value}%")
        elif name == "ThresholdReach":
            duration = self.calculate_duration(value)
            self.durationThresholdLabel.setText(f"{duration:.2f}s")
        elif name == "ThresholdSecond":
            self.procentSecondLabel.setText(f"{value}%")
        elif name == "ThresholdReachSecond":
            duration = self.calculate_duration(value)
            self.durationSecondLabel.setText(f"{duration:.2f}s")

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