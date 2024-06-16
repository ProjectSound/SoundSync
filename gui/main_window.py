from PyQt6.QtCore import Qt, QFile, QIODevice, QTimer
from PyQt6.QtGui import QFontDatabase, QIcon
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from backend.config import Config
from backend.global_state_manager import GlobalStateManager
from gui.custom_titlebar import CustomTitleBar
from gui.animated_stacked_widget import AnimatedStackedWidget
from gui.apps import Apps
from gui.apps_settings import AppsSettings
from gui.bind_create import BindCreate
from gui.bind_remove import BindRemove
from gui.binds import Binds
from gui.binds_clear import BindsClear
from gui.custom_messagebox import CustomMessageBox
from gui.cutoff_modes import CutoffModes
from gui.inputs import Inputs
from gui.inputs_settings import InputsSettings
from gui.menu import Menu
from gui.settings import Settings

from resources.resources import *


class MainWindow(QMainWindow):
    def __init__(self, app, core, actions, binds, cutoff, input_device_manager, audio_session_manager, input_manager,
                 update_sound_manager_app, settings_core, is_silent):
        super().__init__()

        self.loadPoppinsFont()

        self.appTimer = QTimer()
        self.appTimer.setInterval(1000)
        self.app = app

        self.core = core

        self.config = Config()

        self.actions = actions
        self.bindsCore = binds
        self.cutoff = cutoff
        self.input_device_manager = input_device_manager
        self.audio_session_manager = audio_session_manager
        self.input_manager = input_manager
        self.update_sound_manager_app = update_sound_manager_app
        self.settings_core = settings_core

        self.is_silent = is_silent

        self.initUI()

    def initUI(self):

        if self.config.scaleTitlebar:
            self.addToHeight = int(30 * self.config.scale[self.config.selectedScale]['scale'])
        else:
            self.addToHeight = 30

        width = int(600 * self.config.scale[self.config.selectedScale]['scale'])
        height = int(487 * self.config.scale[self.config.selectedScale]['scale'] + self.addToHeight)
        self.setFixedSize(width, height)
        self.center()

        self.setWindowTitle('SilentGuardian')
        self.setObjectName("MainWindow")
        self.setWindowIcon(QIcon(":/app_icon.ico"))
        self.setStyleSheet(
            f"background: {self.config.colorMode[self.config.selectedTheme]['windowBackground']};"
            f"margin: 0; padding: 0; font-family: 'Poppins';")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.title_bar = CustomTitleBar(self, True, True,
                                        "SILENTGUARDIAN", self.config.minimize_to_tray)

        self.windowWidget = QWidget(self)
        self.windowLayout = QVBoxLayout(self.windowWidget)
        self.windowLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.windowWidget)

        self.main_widget = QWidget(self)
        self.main_widget.setFixedSize(width, height)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(10, 0, 10, self.addToHeight + 10)

        self.menu = Menu()
        self.menu.switchTab.connect(self.changeTab)

        self.inputs = Inputs(self.input_device_manager, self.input_manager)
        self.inputs.switchTab.connect(self.changeTab)

        self.inputsSettings = InputsSettings(self.input_manager)
        self.inputsSettings.switchTab.connect(self.changeTab)

        self.apps = Apps(self.audio_session_manager, self.update_sound_manager_app)
        self.apps.switchTab.connect(self.changeTab)

        self.appsSettings = AppsSettings()
        self.appsSettings.switchTab.connect(self.changeTab)

        self.cutoffModes = CutoffModes(self.cutoff)

        self.binds = Binds(self.actions, self.bindsCore)
        self.binds.switchTab.connect(self.changeTab)
        self.binds.showBindRemove.connect(self.showRemoveBind)

        self.bindCreate = BindCreate(self.actions, self.bindsCore)
        self.bindCreate.switchTab.connect(self.changeTab)
        self.bindCreate.bindCreate.connect(self.createBind)

        self.bindRemove = BindRemove(self.actions, self.bindsCore)
        self.bindRemove.switchTab.connect(self.changeTab)
        self.bindRemove.confirmRemoveBind.connect(self.confirmRemoveBind)

        self.bindsClear = BindsClear()
        self.bindsClear.switchTab.connect(self.changeTab)
        self.bindsClear.confirmClearBinds.connect(self.confirmClearBinds)

        self.tab_widget = AnimatedStackedWidget()
        self.tab_widget.addWidget(self.inputs)
        self.tab_widget.addWidget(self.inputsSettings)
        self.tab_widget.addWidget(self.apps)
        self.tab_widget.addWidget(self.appsSettings)
        self.tab_widget.addWidget(self.cutoffModes)
        self.tab_widget.addWidget(self.binds)
        self.tab_widget.addWidget(self.bindCreate)
        self.tab_widget.addWidget(self.bindRemove)
        self.tab_widget.addWidget(self.bindsClear)
        self.tab_widget.addWidget(Settings(self.settings_core))

        self.tab_widget.setCurrentIndex(0)

        self.main_layout.addWidget(self.menu)
        self.main_layout.addWidget(self.tab_widget)

        self.windowLayout.addWidget(self.title_bar)
        self.windowLayout.addWidget(self.main_widget)

        self.appTimer.timeout.connect(self.apps.updateApps)

        # self.showMessageBox()

        GlobalStateManager().runningChanged.connect(self.handle_running_changed)

        if not self.is_silent:
            self.show()
        else:
            self.title_bar.silentApp()

    def handle_running_changed(self):
        self.title_bar.setStatus()
        self.core.handle_running_changed()

    @staticmethod
    def loadPoppinsFont():
        font_files = ['Poppins-Bold.ttf',
                      'Poppins-ExtraBold.ttf',
                      'Poppins-Medium.ttf',
                      'Poppins-Regular.ttf', 'Poppins-SemiBold.ttf']

        for font_file in font_files:
            file = QFile(f":/{font_file}")

            # Check if the file is readable
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                print(f"Cannot read font file: {font_file}")
                continue

            font_data = file.readAll()
            QFontDatabase.addApplicationFontFromData(font_data)

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changeTab(self, index):
        if self.appTimer.isActive:
            self.appTimer.stop()

        if index == 0:
            self.inputs.displaySettings()
            self.inputs.stackedWidget.setCurrentIndex(0)
        elif index == 1:
            self.inputsSettings.changeSlidersPosition()
        elif index == 2:
            self.apps.displaySettings()
            self.appTimer.start()
        elif index == 3:
            self.appsSettings.changeSlidersPosition()
            self.appsSettings.displaySettings()
        elif index == 4:
            self.cutoffModes.changeSliderPosition()
        elif index == 6:
            self.bindCreate.clear_sequence()

        self.tab_widget.setCurrentIndex(index)

    def createBind(self):
        self.binds.createBind()

    def showRemoveBind(self, bindIndex):
        self.tab_widget.setCurrentIndex(7)
        self.bindRemove.showKeybind(bindIndex)

    def confirmRemoveBind(self):
        self.binds.removeBind()
        self.tab_widget.setCurrentIndex(5)

    def confirmClearBinds(self):
        self.binds.clearBinds()
        self.tab_widget.setCurrentIndex(5)

    # MESSAGE BOX EXAMPLES
    # def on_accept_button_clicked(self):
    #     print("Accept button clicked")
    #
    # def on_cancel_button_clicked(self):
    #     print("Cancel button clicked!")
    #
    # def showMessageBox(self):
    #     CustomMessageBox(0, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor',
    #                      [['Accept', 'blue', self.on_accept_button_clicked],
    #                       ['Cancel', 'red', self.on_cancel_button_clicked]])
    #     self.app.exec()
    #     CustomMessageBox(1, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor',
    #                      [['Ok', 'blue', None]])
    #     self.app.exec()
    #     CustomMessageBox(2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor',
    #                      [['Cancel', 'red', self.on_cancel_button_clicked]])
    #     self.app.exec()
