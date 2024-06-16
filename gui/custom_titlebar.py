from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QIcon

from backend.config import Config
from backend.global_state_manager import GlobalStateManager
from gui.tray import Tray


class CustomTitleBar(QWidget):
    def __init__(self, parent, renderToggle, renderMinimize, name, minimize_to_tray=None):
        super().__init__(parent)
        self.config = Config()
        self.parent = parent
        self.renderToggle = renderToggle
        self.renderMinimize = renderMinimize
        self.minimize_to_tray = minimize_to_tray
        self.name = name
        self.state_manager = GlobalStateManager()

        self.margin = 1

        if self.parent.objectName() == "MainWindow":
            self.margin = 0

        self.setContentsMargins(0, 0, 0, 0)

        if self.config.scaleTitlebar:
            self.height = int(30 * self.config.scale[self.config.selectedScale]['scale'])
            self.iconSize = int(16 * self.config.scale[self.config.selectedScale]['scale'])
            self.statusButtonWidth = int(80 * self.config.scale[self.config.selectedScale]['scale'])
            self.statusIconSize = int(12 * self.config.scale[self.config.selectedScale]['scale'])
            self.close_minimalizeWidth = int(36 * self.config.scale[self.config.selectedScale]['scale'])
            self.titleFontSize = self.config.scale[self.config.selectedScale]['font-size-smaller']
            self.statusFontSize = self.config.scale[self.config.selectedScale]['font-size-smallest']
        else:
            self.height = 30
            self.iconSize = 16
            self.statusButtonWidth = 80
            self.statusIconSize = 12
            self.close_minimalizeWidth = 36
            self.titleFontSize = "14px"
            self.statusFontSize = "13px"

        self.setFixedHeight(self.height)

        self.tray = Tray(self.parent)

        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(0)

        icon = QIcon(':/app_icon.ico')
        iconWidget = QLabel()

        pixmap = icon.pixmap(self.iconSize, self.iconSize)
        iconWidget.setPixmap(pixmap)
        iconWidget.setFixedSize(self.iconSize, self.iconSize)

        title = QLabel(self.name)
        title.setStyleSheet(f"font-family: 'Poppins'; font-size: {self.titleFontSize}; font-weight: 800; color: {self.config.colorMode[self.config.selectedTheme]['footerColor']};")
        title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttons = QWidget()
        self.buttons.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.buttonsLayout = QHBoxLayout(self.buttons)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(0)
        self.buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        if self.renderToggle:
            self.statusButton = QPushButton()
            self.statusButton.setFixedSize(self.statusButtonWidth, self.height)
            self.statusButton.setIconSize(QSize(self.statusIconSize, self.statusIconSize))
            self.statusButton.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
            if not self.state_manager.running:
                self.statusButton.setText("START ")
                self.statusButton.setStyleSheet(f"""
                                        QPushButton {{
                                            border: none;
                                            font-family: 'Poppins';
                                            font-weight: 700;
                                            font-size: {self.statusFontSize};
                                            color: #3498DB;
                                        }}
                                        QPushButton:hover {{
                                            background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                                        }}
                                        QPushButton:pressed {{
                                            background-color: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};
                                        }}
                                    """)
                self.statusButton.setIcon(QIcon(':/start.svg'))
            else:
                self.statusButton.setText("STOP ")
                self.statusButton.setStyleSheet(f"""
                                        QPushButton {{
                                            border: none;
                                            font-family: 'Poppins';
                                            font-weight: 700;
                                            font-size: 13px;
                                            color: #EB4D4B;
                                        }}
                                        QPushButton:hover {{
                                            background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                                        }}
                                        QPushButton:pressed {{
                                            background-color: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};
                                        }}
                                    """)
                self.statusButton.setIcon(QIcon(':/stop.svg'))
            self.statusButton.clicked.connect(self.toggleStatus)

        self.minimalizeButton = QPushButton()
        self.minimalizeButton.setStyleSheet(f"""
            QPushButton {{
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
            }}
            QPushButton:pressed {{
                background-color: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};
            }}
        """)
        self.minimalizeButton.setFixedSize(self.close_minimalizeWidth, self.height)
        if self.config.selectedTheme == 0:
            self.minimalizeButton.setIcon(QIcon(':/minimalize.svg'))
        else:
            self.minimalizeButton.setIcon(QIcon(':/minimalize_light.svg'))

        self.minimalizeButton.setIconSize(QSize(self.iconSize, self.iconSize))
        self.minimalizeButton.clicked.connect(lambda: self.window().windowHandle().showMinimized())

        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet(f"""
            QPushButton {{
                 border: none;
            }}
            QPushButton:hover {{
                background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
            }}
            QPushButton:pressed{{
                background-color: #EB4D4B;
            }}
        """)
        self.closeButton.setFixedSize(self.close_minimalizeWidth, self.height)
        if self.config.selectedTheme == 0:
            self.closeButton.setIcon(QIcon(':/close.svg'))
        else:
            self.closeButton.setIcon(QIcon(':/close_light.svg'))

        self.closeButton.setIconSize(QSize(self.iconSize, self.iconSize))
        self.closeButton.clicked.connect(self.closeApp)

        if self.renderToggle:
            self.buttonsLayout.addWidget(self.statusButton)

        if self.renderMinimize:
            self.buttonsLayout.addWidget(self.minimalizeButton)

        self.buttonsLayout.addWidget(self.closeButton)

        self.layout.addWidget(iconWidget)
        self.layout.addWidget(title)
        self.layout.addWidget(self.buttons)

        self.start = QPoint(0, 0)
        self.pressing = False

    def closeApp(self):
        if self.parent.objectName() == "MainWindow":
            if self.config.minimize_to_tray:
                self.tray.show()
                self.parent.hide()
            else:
                QApplication.instance().quit()
        else:
            self.parent.close()

    def silentApp(self):
        self.tray.show()

    def toggleStatus(self):
        if self.state_manager.running:
            self.state_manager.running = False
        else:
            self.state_manager.running = True
        self.setStatus()

    def setStatus(self):
        if not self.state_manager.running:
            self.statusButton.setText("START ")
            self.statusButton.setStyleSheet(f"""
                                    QPushButton {{
                                        border: none;
                                        font-family: 'Poppins';
                                        font-weight: 700;
                                        font-size: {self.statusFontSize};
                                        color: #3498DB;
                                    }}
                                    QPushButton:hover {{
                                        background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                                    }}
                                    QPushButton:pressed {{
                                        background-color: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};
                                    }}
                                """)
            self.statusButton.setIcon(QIcon(':/start.svg'))
        else:
            self.statusButton.setText("STOP ")
            self.statusButton.setStyleSheet(f"""
                                    QPushButton {{
                                        border: none;
                                        font-family: 'Poppins';
                                        font-weight: 700;
                                        font-size: {self.statusFontSize};
                                        color: #EB4D4B;
                                    }}
                                    QPushButton:hover {{
                                        background-color: {self.config.colorMode[self.config.selectedTheme]['widgetBackground']};
                                    }}
                                    QPushButton:pressed {{
                                        background-color: {self.config.colorMode[self.config.selectedTheme]['activeWidget']};
                                    }}
                                """)
            self.statusButton.setIcon(QIcon(':/stop.svg'))

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x() - self.margin,
                                    self.mapToGlobal(self.movement).y() - self.margin,
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
