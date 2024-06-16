from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QGraphicsOpacityEffect


class AnimatedStackedWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        self.animation_duration = 100
        self.current_index = 0
        self.previous_index = 0

    def addWidget(self, widget):
        self.stacked_widget.addWidget(widget)

    def setCurrentIndex(self, index):
        if self.current_index != index:
            self.previous_index = self.current_index
            self.current_index = index

            self.slide()

    def slide(self):
        self.current_widget = self.stacked_widget.widget(self.current_index)
        self.previous_widget = self.stacked_widget.widget(self.previous_index)

        self.currentWidgetEffect = QGraphicsOpacityEffect()
        self.previousWidgetEffect = QGraphicsOpacityEffect()

        self.current_widget.setGraphicsEffect(self.currentWidgetEffect)
        self.currentWidgetEffect.setOpacity(0.2)
        self.previous_widget.setGraphicsEffect(self.previousWidgetEffect)
        self.previousWidgetEffect.setOpacity(1)

        self.current_anim = QPropertyAnimation(self.currentWidgetEffect, b"opacity")
        self.current_anim.setDuration(self.animation_duration)
        self.current_anim.setStartValue(0.2)
        self.current_anim.setEndValue(1)

        self.previous_anim = QPropertyAnimation(self.previousWidgetEffect, b"opacity")
        self.previous_anim.setDuration(self.animation_duration)
        self.previous_anim.setStartValue(1)
        self.previous_anim.setEndValue(0.2)

        if self.previous_index >= 0:
            self.previous_anim.finished.connect(self.startNextAnimation)
            self.previous_anim.start()
        else:
            self.stacked_widget.setCurrentIndex(self.current_index)
            self.current_anim.finished.connect(self.current_anim.deleteLater)
            self.current_anim.start()

    def startNextAnimation(self):
        self.previous_anim.deleteLater()
        self.stacked_widget.setCurrentIndex(self.current_index)
        self.current_anim.start()
        self.current_anim.finished.connect(self.current_anim.deleteLater)