import math

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSlider

from backend.config import Config


class CutoffModes(QWidget):
    def __init__(self, cutoff):
        super().__init__()

        self.config = Config()

        self.cutoff = cutoff

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

        self.cutoffModes = {
            0: "Hard",
            1: "Fade",
            2: "Mute / Unmute",
            3: "Hard cut + fade up",
            4: "Fade down + hard up",
            5: "Mute + fade up",
            6: "Mute + hard up"
        }

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 0, 8, 0)

        # CUTOFF MODES LIST #

        self.modes = QWidget()
        # modes.setFixedWidth(306)
        self.modesLayout = QVBoxLayout(self.modes)
        self.modesLayout.setContentsMargins(5, 0, 5, 0)
        self.modesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header = QLabel("Cutoff modes:")
        header.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.modesLayout.addWidget(header)

        for key, value in self.cutoffModes.items():
            mode_widget = QWidget()
            mode_widget.setObjectName(f"CutoffWidget_{key}")
            mode_widget.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
            mode_layout = QHBoxLayout(mode_widget)
            label = QLabel(value)
            label.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
            mode_widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                f"border-radius: 5px;")

            if key == self.config.selectedCutoff:
                mode_widget.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};"
                    f"border-radius: 5px;")
                label.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                    f"color: #ffffff; font-weight: 700;")

            mode_layout.addWidget(label)

            mode_widget.installEventFilter(self)
            self.modesLayout.addWidget(mode_widget)

        # FADE DURATION #

        self.fade = QWidget()
        self.fadeLayout = QVBoxLayout(self.fade)
        self.fadeLayout.setContentsMargins(5, 0, 7, 0)
        self.fadeLayout.setAlignment(Qt.AlignmentFlag.AlignBaseline)

        label = QLabel("Fade duration:")
        label.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500;"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setFixedHeight(self.sliderHeight)
        # self.slider.setValue(20)
        self.calculate_slider_position(self.config.fade_duration)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.updateValue)
        self.slider.setStyleSheet(f"""
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
        duration.setFixedHeight(int(34 * self.config.scale[self.config.selectedScale]['scale']))
        duration.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                               f"border-radius: 5px;")
        durationLayout = QHBoxLayout(duration)

        self.durationFadeLabel = QLabel("2s")
        self.durationFadeLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; font-weight: 700;"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        self.durationFadeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        durationLayout.addWidget(self.durationFadeLabel)

        if self.config.selectedCutoff == 1 or self.config.selectedCutoff == 3 or self.config.selectedCutoff == 4 or self.config.selectedCutoff == 5:
            self.fade.setVisible(True)
        else:
            self.fade.setVisible(False)

        self.fadeLayout.addWidget(label)
        self.fadeLayout.addWidget(self.slider)
        self.fadeLayout.addWidget(duration)

        self.fadeLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # COMBINE EVERYTHING #

        layout.addWidget(self.modes, 0)
        layout.addWidget(self.fade)

        self.setLayout(layout)

    def calculate_slider_position(self, duration):
        if duration <= 0.5:
            value = 1 + (duration - 0.5) * (20 - 1) / (1 - 0.5)
        elif duration <= 1:
            value = 20 + (duration - 1) * (40 - 20) / (2 - 1)
        elif duration <= 2:
            value = 40 + (duration - 2) * (50 - 40) / (2.5 - 2)
        elif duration <= 2.5:
            value = 50 + (duration - 2.5) * (60 - 50) / (3 - 2.5)
        elif duration <= 3:
            value = 60 + (duration - 3) * (80 - 60) / (4 - 3)
        else:
            value = 80 + (duration - 4) * (100 - 80) / (5 - 4)

        return int(value)

    def updateValue(self, value):
        if value <= 20:
            duration = 0.5 + (value - 1) * (1 - 0.5) / (20 - 1)
        elif value <= 40:
            duration = 1 + (value - 20) * (2 - 1) / (40 - 20)
        elif value <= 50:
            duration = 2 + (value - 40) * (2.5 - 2) / (50 - 40)
        elif value <= 60:
            duration = 2.5 + (value - 50) * (3 - 2.5) / (60 - 50)
        elif value <= 80:
            duration = 3 + (value - 60) * (4 - 3) / (80 - 60)
        else:
            duration = 4 + (value - 80) * (5 - 4) / (100 - 80)

        self.durationFadeLabel.setText(f"{duration:.2f}s")
        self.config.fade_duration = duration
        self.config.save()

    def changeSliderPosition(self):
        self.slider.setSliderPosition(self.calculate_slider_position(self.config.fade_duration))

    def getWidgetByName(self, widget_name):
        return self.modes.findChild(QWidget, widget_name)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # SELECT CUTOFF MODE WITH WHATEVER MOUSE BUTTON #
            key = int(str(watched.objectName()).split("_")[-1])
            if key != self.config.selectedCutoff:
                lastSelectedWidget = self.getWidgetByName(f"CutoffWidget_{self.config.selectedCutoff}")
                widget = self.getWidgetByName(watched.objectName())

                if lastSelectedWidget:
                    lastSelectedWidget.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                        f"border-radius: 5px;")
                    label = lastSelectedWidget.findChild(QLabel)
                    if label:
                        label.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

                if widget:
                    widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};"
                                         f"border-radius: 5px;")
                    label = widget.findChild(QLabel)
                    if label:
                        label.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                            f"color: #ffffff; font-weight: 700;")

                self.config.selectedCutoff = key
                self.cutoff.apply(key)

                if (self.config.selectedCutoff == 1 or self.config.selectedCutoff == 3
                        or self.config.selectedCutoff == 4 or self.config.selectedCutoff == 5):
                    self.fade.setVisible(True)
                else:
                    self.fade.setVisible(False)

        return super().eventFilter(watched, event)
