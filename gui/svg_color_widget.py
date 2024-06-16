from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget, QLabel


class SVGColorWidget(QWidget):
    def __init__(self, svg_path, width, height, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

        color = QColor(color)

        renderer = QSvgRenderer(svg_path)

        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(pixmap)

        renderer.render(painter)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        label = QLabel(self)
        label.setPixmap(pixmap)
