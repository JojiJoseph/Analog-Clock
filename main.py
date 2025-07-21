import sys
import PyQt6
import PyQt6.QtCore
import PyQt6.QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Simple Window")
        self.setGeometry(100, 100, 300, 300)
        self.setWindowFlag(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint, True)
        path = PyQt6.QtGui.QPainterPath()
        rect = self.rect()
        path.addEllipse(
            PyQt6.QtCore.QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        )
        region = PyQt6.QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        self.timer = PyQt6.QtCore.QTimer(self)
        self.timer.timeout.connect(self.print_time)
        self.timer.start(1000)

        # Translucent background
        self.setAttribute(PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.angle = 0

    def mousePressEvent(self, event):
        if event.button() == PyQt6.QtCore.Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & PyQt6.QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def paintEvent(self, event):
        painter = PyQt6.QtGui.QPainter(self)
        painter.setRenderHint(PyQt6.QtGui.QPainter.RenderHint.Antialiasing)
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 10

        # Fill background with translucent color
        bg_color = PyQt6.QtGui.QColor(30, 30, 30, 128)  # RGBA, alpha=128 for 50% translucency
        painter.setBrush(bg_color)
        painter.setPen(PyQt6.QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(self.rect())

        # Draw the second hand
        painter.save()
        painter.translate(center)
        painter.rotate(self.angle)
        pen = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor("red"), 3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, -radius + 30)
        painter.restore()

        # Draw the minute hand
        minutes = PyQt6.QtCore.QTime.currentTime().minute()
        minute_angle = (minutes * 6) % 360  # 360/60 = 6 degrees per minute
        painter.save()
        painter.translate(center)
        painter.rotate(minute_angle)
        pen = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor("blue"), 5)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, -radius + 30)
        painter.restore()

        # Draw the hour hand
        hours = PyQt6.QtCore.QTime.currentTime().hour() % 12
        hour_angle = (
            hours * 30 + minutes / 2
        ) % 360  # 360/12 = 30 degrees per hour, plus half a degree per minute
        painter.save()
        painter.translate(center)
        painter.rotate(hour_angle)
        pen = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor("green"), 7)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, -radius + 40)
        painter.restore()

        # Draw the labels from 1 to 12
        for i in range(1, 13):
            angle = (i * 30) % 360
            painter.save()
            pen = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor("white"), 2)
            painter.setPen(pen)
            painter.translate(center)
            painter.rotate(angle)
            painter.translate(0, -radius + 10)
            painter.rotate(-angle)
            painter.drawText(-10, 0, str(i))
            painter.restore()

    def print_time(self):
        seconds = PyQt6.QtCore.QTime.currentTime().second() % 60
        self.angle = seconds * 6  # 360/60 = 6 degrees per second
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
