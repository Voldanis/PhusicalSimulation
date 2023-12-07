import time
from math import ceil

from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QKeyEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from classes import Measurement
from settings import MeasurementsSettings, ToggleSettings
from utils import Pointer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.canvas_width = 600
        self.canvas_height = 480
        self.measurements = {"1D": Measurement(1, 0, 0), "2D": Measurement(2, 0, 0)}
        self.cur_measurement = Pointer(self.measurements["1D"])
        self.values = 11
        self.fps = 10

        self.init_ui()
    
    def init_ui(self):        
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = QLabel()
        layout.addWidget(self.canvas, 0, 1)

        self.timer = QtCore.QTimer()
        #self.start_timer()

        settings_widget = QWidget()
        settings_widget.setMaximumWidth(160)
        layout.addWidget(settings_widget, 0, 0)

        settings = QVBoxLayout(settings_widget)
        settings.setContentsMargins(8, 8, 8, 8)

        measures_settings = MeasurementsSettings(
            self.measurements, self.cur_measurement,
            self.draw_measurement
        )
        toggle_widget = ToggleSettings(measures_settings, None)

        settings.addWidget(toggle_widget)
        settings.addWidget(measures_settings)

        self.draw_measurement(+self.cur_measurement)

        self.setFocus()
        self.show()

    def draw_measurement(self, measure: 'Measurement'):
        canvas = QPixmap(self.canvas_width, self.canvas_height)

        canvas.fill(QColor("white"))
        painter = QPainter(canvas)
        painter.setBrush(QtCore.Qt.GlobalColor.black)
        
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor("black"))
        painter.setPen(pen)

        font = QFont()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)
        offset = 15
        if measure.dimensions_num == 1:
            unit = ceil((canvas.width() - 30) // (self.values - 1) * measure.scale)
            painter.drawLine(0, canvas.height() // 2,
                             canvas.width(), canvas.height() // 2)
            for i in range(ceil(canvas.width() / unit)):
                painter.drawLine(i * unit + offset, canvas.height() // 2,
                                 i * unit + offset, canvas.height() // 2 + 10)
                painter.drawText(i * unit + offset - 3, canvas.height() // 2 + 22,
                                 str(measure.cam_x + i))
            for obj in measure.objects:
                obj.draw(painter, unit, offset, canvas, measure)
        elif measure.dimensions_num == 2:
            unit = ceil((canvas.width() - 30) // (self.values - 1) * measure.scale)
            painter.drawLine(-measure.cam_x * unit + offset, 0,
                             -measure.cam_x * unit + offset, canvas.height())  # Vertical
            painter.drawLine(0, canvas.height() + measure.cam_y * unit - offset,
                             canvas.width(), canvas.height() + measure.cam_y * unit - offset)  # Horizontal
            painter.setPen(QtCore.Qt.PenStyle.DotLine)
            for i in range(ceil(canvas.width() / unit)):  # Dotted lines
                # Horizontal
                painter.drawLine(0, canvas.height()-offset - i * unit,
                                 canvas.width(), canvas.height()-offset - i * unit)
                painter.drawText(0, canvas.height()-offset - i * unit, str(measure.cam_y + i))
                # Vertical
                painter.drawLine(i * unit + offset, 0,
                                 i * unit + offset, canvas.height())
                painter.drawText(i * unit + offset+2, canvas.height()-2, str(measure.cam_x + i))
            painter.setPen(QtCore.Qt.PenStyle.SolidLine)
            for obj in measure.objects:
                obj.draw(painter, unit, offset, canvas, measure)
        painter.end()

        self.canvas.setPixmap(canvas)

    def start_timer(self):
        self.timer.timeout.connect(self.iteration)
        (+self.cur_measurement).time = time.time()
        self.timer.start(int(1000 / self.fps))

    def iteration(self):
        t = time.time() - (+self.cur_measurement).time
        for i in (+self.cur_measurement).objects:
            i.simulate(t)
        self.draw_measurement(+self.cur_measurement)

    def keyPressEvent(self, event: QKeyEvent):
        measure = +self.cur_measurement

        match event.key():
            case QtCore.Qt.Key.Key_A:
                measure.cam_x -= measure.scale
            case QtCore.Qt.Key.Key_D:
                measure.cam_x += measure.scale
            case QtCore.Qt.Key.Key_S:
                measure.cam_y -= measure.scale
            case QtCore.Qt.Key.Key_W:
                measure.cam_y += measure.scale
            case QtCore.Qt.Key.Key_Equal:
                measure.scale *= 1.1
            case QtCore.Qt.Key.Key_Minus:
                measure.scale /= 1.1
            case QtCore.Qt.Key.Key_Escape:
                self.setFocus()

        self.draw_measurement(+self.cur_measurement)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
