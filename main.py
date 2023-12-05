import time
from math import ceil

from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from classes import Measurement, Point


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.canvas_width = 600
        self.canvas_height = 480
        self.measurements = {"1D": Measurement(1, 0, 0), "2D": Measurement(2, 0, 0)}
        self.cur_measurement = self.measurements["1D"]
        self.values = 11
        self.fps = 10

        self.cur_measurement.objects.append(Point(0, 0, 10, 0, 0, 0, 0, 0))

        self.init_ui()
    
    def init_ui(self):        
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel()
        layout.addWidget(self.label, 0, 1)

        self.timer = QtCore.QTimer()
        #self.start_timer()

        settings = QWidget()
        settings.setMaximumWidth(160)

        self.settings = QVBoxLayout(settings)
        self.settings.setContentsMargins(8, 8, 8, 8)
        self.settings.setAlignment(QtCore.Qt.AlignmentFlag.AlignAbsolute)

        measure_box = QComboBox()
        measure_box.addItems([*self.measurements.keys(), "Добавить среду..."])
        measure_box.activated[str].connect(self.measure_box_changed)
        measure_box.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.settings.addWidget(measure_box)
        
        layout.addWidget(settings, 0, 0)

        self.create_measure = QWidget()
        create_measure = QGridLayout(self.create_measure)
        create_measure.setContentsMargins(0, 0, 0, 0)

        line_name = QLineEdit()
        line_name.setPlaceholderText("Name")
        line_d = QLineEdit()
        line_d.setPlaceholderText("Dimensions")
        button_create = QPushButton("Create")
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.measurement_cancel)

        create_measure.addWidget(line_name, 0, 0, 1, 2)
        create_measure.addWidget(line_d, 1, 0, 1, 2)
        create_measure.addWidget(button_create, 2, 0)
        create_measure.addWidget(button_cancel, 2, 1)
        create_measure.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)

        self.draw_measurement(self.cur_measurement)
        
        self.show()

    def measure_box_changed(self, text: str):
        if text == "Добавить среду...":
            self.settings.addWidget(self.create_measure)
            self.create_measure.show()
        else:
            measurement = self.measurements.get(text)
            if measurement is None:
                return
            self.cur_measurement = measurement
            self.draw_measurement(measurement)
        
    def measurement_cancel(self):
        self.settings.removeWidget(self.create_measure)
        self.create_measure.hide()

    def draw_measurement(self, measure: 'Measurement'):
        canvas = QPixmap(self.canvas_width, self.canvas_height)

        canvas.fill(QColor('white'))
        painter = QPainter(canvas)
        painter.setBrush(QtCore.Qt.GlobalColor.black)
        
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor('black'))
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

        self.label.setPixmap(canvas)

    def start_timer(self):
        self.timer.timeout.connect(self.iteration)
        self.cur_measurement.time = time.time()
        self.timer.start(int(1000 / self.fps))

    def iteration(self):
        t = time.time() - self.cur_measurement.time
        for i in self.cur_measurement.objects:
            i.simulate(t)
        self.draw_measurement(self.cur_measurement)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_A:
            self.cur_measurement.cam_x -= 1
        elif event.key() == QtCore.Qt.Key.Key_D:
            self.cur_measurement.cam_x += 1
        elif event.key() == QtCore.Qt.Key.Key_S:
            self.cur_measurement.cam_y -= 1
        elif event.key() == QtCore.Qt.Key.Key_W:
            self.cur_measurement.cam_y += 1
        elif event.key() == QtCore.Qt.Key.Key_Equal:
            self.cur_measurement.scale *= 1.1
        elif event.key() == QtCore.Qt.Key.Key_Minus:
            self.cur_measurement.scale /= 1.1
        self.draw_measurement(self.cur_measurement)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    app.exec()
