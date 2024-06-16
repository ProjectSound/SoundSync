import math
from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea

from backend.config import Config
from gui.svg_color_widget import SVGColorWidget


class Apps(QWidget):
    switchTab = pyqtSignal(int)

    def __init__(self, audio_session_manager, update_sound_manager_app):
        super().__init__()

        self.config = Config()

        self.audio_session_manager = audio_session_manager
        self.update_sound_manager_app = update_sound_manager_app

        self.iconSize = int(28 * self.config.scale[self.config.selectedScale]['scale'])
        self.infoWidgetSize = int(120 * self.config.scale[self.config.selectedScale]['scale'])

        self.lastAppList = self.audio_session_manager.list_applications().copy()
        self.lastSelectedApp = self.audio_session_manager.selectedAppKey

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

        icon = SVGColorWidget(':/input.svg', self.iconSize, self.iconSize, self.config.colorMode[self.config.selectedTheme]['text-color'])

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

        normalVolumeWidget.mousePressEvent = partial(self.emitSignal, index=3)

        # LOW VOLUME #

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

        lowVolumeWidget.mousePressEvent = partial(self.emitSignal, index=3)

        # LINE (SEPARATOR) #

        line = QFrame()
        line.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['lineColor']};")
        line.setFixedSize(int(275 * self.config.scale[self.config.selectedScale]['scale']), 1)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # APP LIST #

        self.apps = QWidget()
        self.appsLayout = QVBoxLayout(self.apps)
        self.appsLayout.setContentsMargins(5, 0, 5, 0)
        self.appsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.appsLayout.setSpacing(int(5 * self.config.scale[self.config.selectedScale]['scale']))

        header = QLabel("Apps:")
        header.setFixedHeight(int(30 * self.config.scale[self.config.selectedScale]['scale']))
        header.setStyleSheet(
            f"font-family: 'Poppins'; font-size: {self.config.scale[self.config.selectedScale]['font-size-bigger']};"
            f"font-weight: 500; color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        header.setContentsMargins(5, 0, 0, 0)

        for key, value in self.audio_session_manager.list_applications().items():
            self.appsLayout.addWidget(self.appWidget(key, value))

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
        scroll_area.setWidget(self.apps)

        # COMBINE EVERYTHING #

        infoLayout.addWidget(normalVolumeWidget)
        infoLayout.addWidget(lowVolumeWidget)

        layout.addWidget(info)
        layout.addWidget(line, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)
        layout.addWidget(scroll_area)

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

        self.setLayout(layout)

    def emitSignal(self, event, index):
        self.switchTab.emit(index)

    def displaySettings(self):
        self.procentNormalLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.normal_sound_level}%</font>")
        self.procentLowLabel.setText(
            f"<font color='{self.config.colorMode[self.config.selectedTheme]['primaryColor']}'>{self.config.reduced_sound_level}%</font>")

    def appWidget(self, key: str, name: str, missing=False) -> QWidget:
        message = None
        app_widget = QWidget()
        app_widget.setObjectName(f"AppWidget_{key}")
        app_widget.setFixedHeight(int(36 * self.config.scale[self.config.selectedScale]['scale']))
        app_layout = QHBoxLayout(app_widget)
        label = QLabel(f"{name}")
        label.setStyleSheet(
            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
            f"color: {self.config.colorMode[self.config.selectedTheme]['text-color']};")
        label.setContentsMargins(10, 0, 10, 0)
        app_widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};"
                                 f"border-radius: 5px;")

        if str(name + ".exe") == self.config.selectedApp:
            app_widget.setStyleSheet(f"background: {self.config.colorMode[self.config.selectedTheme]['primaryColor']};"
                                     f"border-radius: 5px;")
            label.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                f"color: #ffffff; font-weight: 700;")

        if missing:
            app_widget.setStyleSheet("background: #FF4757; border-radius: 5px;")
            label.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                f"color: #ffffff; font-weight: 700;")
            message = QLabel("NOT FOUND")
            message.setObjectName("message")
            message.setStyleSheet(
                f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smallest']};"
                f"color: #ffffff; font-weight: 700;")
            message.setContentsMargins(10, 0, 10, 0)
            message.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        app_layout.addWidget(label)
        if missing:
            app_layout.addWidget(message)
        else:
            app_widget.installEventFilter(self)

        return app_widget

    def updateApps(self):
        try:
            app_list = self.audio_session_manager.list_applications().copy()
            if app_list != self.lastAppList:
                for i in range(self.appsLayout.count()):
                    child = self.appsLayout.itemAt(i).widget()
                    if child:
                        child.deleteLater()

                if self.lastSelectedApp is not None and self.lastSelectedApp not in app_list.keys():
                    self.audio_session_manager.selectedAppKey = None
                    self.appsLayout.addWidget(
                        self.appWidget(self.lastSelectedApp, self.lastAppList[self.lastSelectedApp], True))
                    self.lastSelectedApp = None

                for key, value in app_list.items():
                    if self.audio_session_manager.selectedAppKey == key:
                        self.lastSelectedApp = self.audio_session_manager.selectedAppKey
                    self.appsLayout.addWidget(self.appWidget(key, value))

                self.lastAppList = app_list
        except Exception as e:
            print(e)

    def getWidgetByName(self, widget_name):
        return self.apps.findChild(QWidget, widget_name)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # SELECT APP WITH WHATEVER MOUSE BUTTON #
            key = str(watched.objectName()).split("_")[-1]
            app_name = None
            if key != self.lastSelectedApp:
                lastSelectedWidget = self.getWidgetByName(f"AppWidget_{self.lastSelectedApp}")
                widget = self.getWidgetByName(watched.objectName())

                if lastSelectedWidget:
                    message = lastSelectedWidget.findChild(QLabel, "message")
                    if message:
                        lastSelectedWidget.deleteLater()
                    else:
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
                        app_name = label.text()
                        label.setStyleSheet(
                            f"font-size: {self.config.scale[self.config.selectedScale]['font-size-smaller']};"
                            f"color: #ffffff; font-weight: 700;")

                self.config.selectedApp = str(app_name + ".exe")
                self.update_sound_manager_app()
                self.lastSelectedApp = key
                self.config.save()

        return super().eventFilter(watched, event)
