import sys
import time
from math import ceil

from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from canvas import Canvas
from physic_models import Measurement, Vector
from settings import MeasurementsSettings, ObjectsSettings, TimeSettings, ToggleSettings
from utils import Pointer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.measurements = {"1D": Measurement(1, 0, 0), "2D": Measurement(2, 0, 0)}
        self.cur_measurement = Pointer(self.measurements["1D"])
        self.fps = 60

        self.init_ui()
    
    def init_ui(self):        
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        canvas = Canvas(600, 480, 11, self.cur_measurement)
        self.draw_measurement = canvas.draw_measurement
        layout.addWidget(canvas, 0, 1)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000 // self.fps)
        self.timer.timeout.connect(self.iteration)

        settings_widget = QWidget()
        settings_widget.setMaximumWidth(160)
        layout.addWidget(settings_widget, 0, 0)

        settings = QVBoxLayout(settings_widget)
        settings.setContentsMargins(8, 8, 8, 8)

        time_settings = TimeSettings(self.start_timer, self.stop_timer)
        measures_settings = MeasurementsSettings(
            self.measurements, self.cur_measurement, self.draw_measurement
        )
        self.cur_g = measures_settings.get_var_g_pointer()
        objects_settings = ObjectsSettings(
            self, self.cur_measurement, self.draw_measurement
        )
        toggle_widget = ToggleSettings(measures_settings, objects_settings)

        settings.addWidget(time_settings)
        settings.addWidget(toggle_widget)
        settings.addWidget(measures_settings)
        settings.addWidget(objects_settings)

        self.draw_measurement(+self.cur_measurement)

        self.setFocus()
        self.show()

    def start_timer(self):
        (+self.cur_measurement).time = time.time()
        self.timer.start()
    
    def stop_timer(self):
        self.timer.stop()

    def iteration(self):
        dt = time.time() - (+self.cur_measurement).time
        for obj in (+self.cur_measurement).objects:
            obj.simulate(dt, Vector(0, -+self.cur_g))
        (+self.cur_measurement).time = time.time()

        self.draw_measurement(+self.cur_measurement)

    def keyPressEvent(self, event: QKeyEvent):
        measure = +self.cur_measurement
        step = ceil(1/measure.scale)

        match event.key():
            case QtCore.Qt.Key.Key_A:
                measure.cam_x -= step
            case QtCore.Qt.Key.Key_D:
                measure.cam_x += step
            case QtCore.Qt.Key.Key_S:
                measure.cam_y -= step
            case QtCore.Qt.Key.Key_W:
                measure.cam_y += step
            case QtCore.Qt.Key.Key_Equal:
                measure.scale *= 1.1
            case QtCore.Qt.Key.Key_Minus:
                measure.scale /= 1.1
            case QtCore.Qt.Key.Key_Escape:
                self.setFocus()

        self.draw_measurement(+self.cur_measurement)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
