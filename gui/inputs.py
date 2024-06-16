import math
import re
from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QStackedWidget, QScrollArea

from backend.config import Config
from gui.svg_color_widget import SVGColorWidget


class Inputs(QWidget):
    switchTab = pyqtSignal(int)

    def __init__(self, input_device_manager, input_manager):
        super().__init__()

        self.config = Config()

        self.iconSize = int(28 * self.config.scale[self.config.selectedScale]['scale'])
        self.infoWidgetSize = int(120 * self.config.scale[self.config.selectedScale]['scale'])

        self.tipHeight = int(64 * self.config.scale[self.config.selectedScale]['scale'])
        self.infoButtonSize = int(18 * self.config.scale[self.config.selectedScale]['scale'])

        self.tips = False

        self.input_device_manager = input_device_manager
        self.input_manager = input_manager

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        info = QWidget()
        infoLayout = QHBoxLayout(info)

        # THRESHOLD #

        thresholdWidget = QWidget()
        thresholdWidget.setFixedSize(self.infoWidgetSize, self.infoWidgetSize)
        thresholdWidget.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        thresholdLayout = QVBoxLayout(thresholdWidget)
        thresholdLayout.setContentsMargins(0, 0, 0, 0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerLayout.setSpacing(0)
        iconContainerWidget.setContentsMargins(0, 5, 0, 0)

        icon = SVGColorWidget(':/threshold.svg', self.iconSize, self.iconSize,
                              self.config.colorMode[self.config.selectedTheme]['text-color'])

        label = QLabel("Threshold")
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.procentLabel = QLabel()
        self.procentLabel.setContentsMargins(0, 0, 0, 5)
        self.procentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.procentLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>50%</font><font color='{self.config.colorMode[self.config.selectedTheme]['text-color']}'>, </font><font color='{self.config.colorMode[self.config.selectedTheme]['secondaryColor']}'>30%</font>")
        self.procentLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 700;")

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)
        iconContainerLayout.addWidget(self.procentLabel)

        thresholdLayout.addWidget(iconContainerWidget)

        thresholdWidget.mousePressEvent = partial(self.emitSignal, index=1)

        # THRESHOLD NOT REACHED #

        thresholdNotReachedWidget = QWidget()
        thresholdNotReachedWidget.setFixedSize(self.infoWidgetSize, self.infoWidgetSize)
        thresholdNotReachedWidget.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 10px;")
        thresholdNotReachedLayout = QVBoxLayout(thresholdNotReachedWidget)
        thresholdNotReachedLayout.setContentsMargins(0, 0, 0, 0)

        iconContainerWidget = QWidget()
        iconContainerLayout = QVBoxLayout(iconContainerWidget)
        iconContainerLayout.setSpacing(0)

        icon = SVGColorWidget(':/stopwatch.svg', self.iconSize, self.iconSize,
                              self.config.colorMode[self.config.selectedTheme]['text-color'])
        icon.setFixedSize(self.iconSize, self.iconSize)

        label = QLabel("Threshold not reached")
        label.setStyleSheet(
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 400;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)

        self.durationLabel = QLabel()
        self.durationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.durationLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>5s</font><font color='{self.config.colorMode[self.config.selectedTheme]['text-color']}'>, </font><font color='{self.config.colorMode[self.config.selectedTheme]['secondaryColor']}'>2s</font>")
        self.durationLabel.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 700;")

        iconContainerLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        iconContainerLayout.addWidget(label)
        iconContainerLayout.addWidget(self.durationLabel)

        thresholdNotReachedLayout.addWidget(iconContainerWidget)

        thresholdNotReachedWidget.mousePressEvent = partial(self.emitSignal, index=1)

        # LINE (SEPARATOR) #

        line = QFrame()
        line.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line.setFixedSize(int(275 * self.config.scale[self.config.selectedScale]['scale']), 1)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # INPUT LIST #

        self.stackedWidget = QStackedWidget()

        self.inputs = QWidget()
        self.inputsLayout = QVBoxLayout(self.inputs)
        self.inputsLayout.setContentsMargins(5, 0, 5, 0)
        self.inputsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.inputsLayout.setSpacing(int(5 * self.config.scale[self.config.selectedScale]['scale']))

        header = QWidget()
        headerLayout = QHBoxLayout(header)
        headerLayout.setContentsMargins(0, 0, 0, 0)

        headerLabel = QLabel("Inputs:")
        headerLabel.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        headerLabel.setContentsMargins(5, 0, 0, 0)
        headerLabel.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']}; font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        infoButton = SVGColorWidget(":/info.svg", self.infoButtonSize, self.infoButtonSize,
                                    self.config.colorMode[self.config.selectedTheme]['text-color'])
        infoButton.setContentsMargins(0, 0, 10, 0)
        infoButton.mousePressEvent = self.toggleTips

        headerLayout.addWidget(headerLabel)
        headerLayout.addWidget(infoButton)

        for input in self.input_device_manager.get_input_devices():
            input_widget = QWidget()
            input_widget.setObjectName(f"InputWidget_{input['index']}")
            input_layout = QVBoxLayout(input_widget)
            input_layout.setSpacing(0)
            matches = re.split(r'\((.*?)\)', input['name'])
            label_name = QLabel()
            label_name.setObjectName('label_name')
            label_extended = QLabel()
            label_extended.setObjectName('label_extended')

            if len(matches) >= 2:
                text_outside = matches[0].strip()
                text_inside = matches[1].strip()

                label_name.setText(f"{text_outside}")
                label_extended.setText(f"({text_inside})")
            else:
                label_name.setText(f"{input['name']}")

            label_name.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
            input_widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
            if len(matches) >= 2:
                label_extended.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

            if input['index'] == self.config.selectedInput1:
                input_widget.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']}; border-radius: 5px;")
                label_name.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
                if len(matches) >= 2:
                    label_extended.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: #ffffff; font-weight: 600;")
            elif input['index'] == self.config.selectedInput2:
                input_widget.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
                label_name.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
                if len(matches) >= 2:
                    label_extended.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: #ffffff; font-weight: 600;")

            input_layout.addWidget(label_name)
            input_layout.addWidget(label_extended) if len(matches) >= 2 else None

            input_widget.installEventFilter(self)
            self.inputsLayout.addWidget(input_widget)

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
        scroll_area.setWidget(self.inputs)

        # INPUT TIPS #

        tips = QWidget()
        tipsLayout = QVBoxLayout(tips)
        tipsLayout.setContentsMargins(5, 0, 5, 0)
        # tipsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        tipNames = [
            'Select First Input',
            'Select Second Input',
            'Swap Inputs',
            'Deselect Second Input'
        ]
        tipMouseIcons = {
            0: {'path': ':/left.svg', 'width': 26, 'height': 36},
            1: {'path': ':/right.svg', 'width': 26, 'height': 36},
            2: {'path': ':/mouse-double-click-left.svg', 'width': 32, 'height': 36},
            3: {'path': ':/mouse-double-click-right.svg', 'width': 32, 'height': 36}
        }

        # LOOP FOR TIPS #

        for i in range(4):
            tipWidget = QWidget()
            tipLayout = QHBoxLayout(tipWidget)
            tipLayout.setContentsMargins(0, 0, 0, 0)
            tipLayout.setSpacing(0)
            tipLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            mouseTile = QWidget()
            mouseTile.setFixedSize(self.tipHeight, self.tipHeight)
            mouseTileLayout = QVBoxLayout(mouseTile)
            mouseTile.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['tipMouseWidget']};"
                                    "border-top-left-radius: 10px;"
                                    "border-top-right-radius: 0px;"
                                    "border-bottom-left-radius: 10px;"
                                    "border-bottom-right-radius: 0px;")
            mouseIcon = SVGColorWidget(tipMouseIcons[i]['path'],
                                       int(tipMouseIcons[i]['width'] * self.config.scale[self.config.selectedScale][
                                           'scale']),
                                       int(tipMouseIcons[i]['height'] * self.config.scale[self.config.selectedScale][
                                           'scale']),
                                       self.config.colorMode[self.config.selectedTheme]['text-color'])
            if i == 1:
                mouseTileLayout.setContentsMargins(6, 0, 0, 0)

            mouseTileLayout.addWidget(mouseIcon)
            mouseTileLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            whatDo = QWidget()
            whatDo.setFixedHeight(self.tipHeight)
            whatDo.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['tipBackground']};"
                                 "border-top-left-radius: 0px;"
                                 "border-top-right-radius: 10px;"
                                 "border-bottom-left-radius: 0px;"
                                 "border-bottom-right-radius: 10px;")
            whatDoLayout = QVBoxLayout(whatDo)
            whatDoLayout.setSpacing(0)
            whatDoLayout.setContentsMargins(8, 0, 8, 0)

            label = QLabel(tipNames[i])
            label.setFixedHeight(int(20 * self.config.scale[self.config.selectedScale]['scale']))
            label.setStyleSheet(
                f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}")

            whatDoLayout.addWidget(label)

            if i == 0 or i == 1:
                inputTile = QWidget()
                inputTileLayout = QHBoxLayout(inputTile)
                inputLabel = QLabel(f"Input {i + 1}")
                inputTile.setFixedHeight(int(32 * self.config.scale[self.config.selectedScale]['scale']))
                if i == 0:
                    inputTile.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']}; border-radius: 5px;")
                else:
                    inputTile.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
                inputLabel.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")

                inputTileLayout.addWidget(inputLabel)

                whatDoLayout.addWidget(inputTile)
            elif i == 2 or i == 3:
                twoInputs = QWidget()
                twoInputsLayout = QHBoxLayout(twoInputs)
                twoInputsLayout.setContentsMargins(0, 0, 0, 0)

                inputTile = QWidget()
                inputTileLayout = QHBoxLayout(inputTile)
                inputTile.setFixedHeight(int(32 * self.config.scale[self.config.selectedScale]['scale']))
                if i == 2:
                    inputLabel = QLabel("Input 1")
                    inputTile.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']}; border-radius: 5px;")
                else:
                    inputLabel = QLabel("Input 2")
                    inputTile.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
                inputLabel.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")

                inputTileLayout.addWidget(inputLabel)

                betweenIcon = QWidget()
                betweenIconLayout = QHBoxLayout(betweenIcon)
                betweenIconLayout.setContentsMargins(0, 0, 0, 0)

                if i == 2:
                    icon = SVGColorWidget(":/swap.svg", int(24 * self.config.scale[self.config.selectedScale]['scale']),
                                          int(20 * self.config.scale[self.config.selectedScale]['scale']),
                                          self.config.colorMode[self.config.selectedTheme]['text-color'])
                    betweenIcon.setFixedSize(int(24 * self.config.scale[self.config.selectedScale]['scale']),
                                             int(20 * self.config.scale[self.config.selectedScale]['scale']))
                else:
                    icon = SVGColorWidget(":/right-arrow.svg",
                                          int(16 * self.config.scale[self.config.selectedScale]['scale']),
                                          int(12 * self.config.scale[self.config.selectedScale]['scale']),
                                          self.config.colorMode[self.config.selectedTheme]['text-color'])
                    betweenIcon.setFixedSize(int(24 * self.config.scale[self.config.selectedScale]['scale']),
                                             int(12 * self.config.scale[self.config.selectedScale]['scale']))

                betweenIconLayout.addWidget(icon)
                betweenIconLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                inputTile2 = QWidget()
                inputTile2Layout = QHBoxLayout(inputTile2)
                inputLabel2 = QLabel("Input 2")
                inputTile2.setFixedHeight(int(32 * self.config.scale[self.config.selectedScale]['scale']))
                if i == 2:
                    inputTile2.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
                    inputLabel2.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
                else:
                    inputTile2.setStyleSheet(
                        f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px; border: 1px solid {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
                    inputLabel2.setStyleSheet(
                        f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']}; font-weight: 400; border: none;")

                inputTile2Layout.addWidget(inputLabel2)

                twoInputsLayout.addWidget(inputTile)
                twoInputsLayout.addWidget(betweenIcon)
                twoInputsLayout.addWidget(inputTile2)

                whatDoLayout.addWidget(twoInputs)

            whatDoLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            tipLayout.addWidget(mouseTile)
            tipLayout.addWidget(whatDo)

            tipsLayout.addWidget(tipWidget)

        self.stackedWidget.addWidget(scroll_area)
        self.stackedWidget.addWidget(tips)

        self.stackedWidget.setCurrentIndex(0)

        # COMBINE EVERYTHING #

        infoLayout.addWidget(thresholdWidget)
        infoLayout.addWidget(thresholdNotReachedWidget)

        layout.addWidget(info)
        layout.addWidget(line, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)
        layout.addWidget(self.stackedWidget)

        bottomMargin = 8

        if self.config.selectedScale == 1:
            bottomMargin = 14
        elif self.config.selectedScale == 2:
            bottomMargin = 16
        elif self.config.selectedScale == 3:
            bottomMargin = 18
        elif self.config.selectedScale == 4:
            bottomMargin = 20
        else:
            bottomMargin = 8

        layout.setContentsMargins(8, 0, 8, bottomMargin)

        self.displaySettings()

        self.setLayout(layout)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def displaySettings(self):
        self.procentLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.threshold1}%</font><font color='{self.config.colorMode[self.config.selectedTheme]['text-color']}'>, </font><font color='{self.config.colorMode[self.config.selectedTheme]['secondaryColor']}'>{self.config.threshold2}%</font>")
        self.durationLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.threshold_not_reached1:.2f}s</font><font color='{self.config.colorMode[self.config.selectedTheme]['text-color']}'>, </font><font color='{self.config.colorMode[self.config.selectedTheme]['secondaryColor']}'>{self.config.threshold_not_reached2:.2f}s</font>")

    def toggleTips(self, event):
        if self.tips:
            self.tips = False
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.tips = True
            self.stackedWidget.setCurrentIndex(1)

    def getWidgetByName(self, widget_name):
        return self.inputs.findChild(QWidget, widget_name)

    def selectInput(self, watched, lastKey=None, button=None):
        widget = self.getWidgetByName(watched.objectName())

        if lastKey or lastKey == 0:
            lastSelectedWidget = self.getWidgetByName(f"InputWidget_{lastKey}")
            labelLastSelectedName = lastSelectedWidget.findChild(QLabel, "label_name") if lastSelectedWidget else None
            labelLastSelectedExtended = lastSelectedWidget.findChild(QLabel,
                                                                     "label_extended") if lastSelectedWidget else None
        else:
            lastSelectedWidget = None
            labelLastSelectedName = None
            labelLastSelectedExtended = None

        labelWidgetName = widget.findChild(QLabel, "label_name")
        labelWidgetExtended = widget.findChild(QLabel, "label_extended")

        if lastSelectedWidget and labelLastSelectedName:
            lastSelectedWidget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
            labelLastSelectedName.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
            if labelLastSelectedExtended:
                labelLastSelectedExtended.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

        if button == 'Right':
            widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
            labelWidgetName.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
            if labelWidgetExtended:
                labelWidgetExtended.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: #ffffff; font-weight: 600;")
        elif button == 'Left':
            widget.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']}; border-radius: 5px;")
            labelWidgetName.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: #ffffff; font-weight: 700;")
            if labelWidgetExtended:
                labelWidgetExtended.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: #ffffff; font-weight: 600;")
        elif button == 'DoubleClick':
            if self.config.selectedInput2 is not None:
                firstInput = self.getWidgetByName(f"InputWidget_{self.config.selectedInput1}")
                secondInput = self.getWidgetByName(f"InputWidget_{self.config.selectedInput2}")
                firstInput.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['secondaryColor']}; border-radius: 5px;")
                secondInput.setStyleSheet(
                    f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']}; border-radius: 5px;")
        elif button == 'UncheckInput2':
            secondInput = self.getWidgetByName(watched.objectName())
            secondInput.setStyleSheet(
                f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']}; border-radius: 5px;")
            labelWidgetName = secondInput.findChild(QLabel, "label_name")
            labelWidgetName.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
            if labelWidgetExtended:
                labelWidgetExtended = secondInput.findChild(QLabel, "label_extended")
                labelWidgetExtended.setStyleSheet(
                    f"font-size: {self.config.scale[self.config.selectedScale]['font-size-footer']}; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")

    def eventFilter(self, watched, event):
        key = int(str(watched.objectName()).split("_")[-1])
        if event.type() == QEvent.Type.MouseButtonPress:
            # LEFT CLICK SELECT INPUT 1 #
            if event.button() == Qt.MouseButton.LeftButton and key != self.config.selectedInput2:
                if self.config.selectedInput1 != key:
                    self.selectInput(watched, self.config.selectedInput1, 'Left')
                    self.config.selectedInput1 = key
                    self.input_manager.change_device(self.input_manager.get_primary())
            # RIGHT CLICK SELECT INPUT 2 #
            elif event.button() == Qt.MouseButton.RightButton and key != self.config.selectedInput1:
                if self.config.selectedInput2 != key and self.config.selectedInput2 is not None:
                    self.selectInput(watched, self.config.selectedInput2, 'Right')
                    self.config.selectedInput2 = key
                    self.input_manager.change_device(self.input_manager.get_secondary())
                else:
                    if self.config.selectedInput2 is None:
                        self.config.selectedInput2 = key
                        self.input_manager.create(self.config.selectedInput2, self.config.threshold2,
                                                  self.config.threshold_not_reached2, False)
                        self.selectInput(watched, None, 'Right')
                    else:
                        # DESELECT INPUT 2 #
                        self.config.selectedInput2 = None
                        self.selectInput(watched, None, 'UncheckInput2')
                        self.input_manager.remove(self.input_manager.get_secondary())
        # DOUBLE CLICK LEFT MOUSE BUTTON SWAP INPUTS #
        elif event.type() == QEvent.Type.MouseButtonDblClick:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.config.selectedInput2 is not None and (key == self.config.selectedInput1 or key == self.config.selectedInput2):
                    self.selectInput(watched, None, 'DoubleClick')
                    self.input_manager.swap_inputs()

        self.config.save()
        return super().eventFilter(watched, event)
