import time

from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 600
        self.height = 480
        self.measurements = {"None": Measurement(0, 0, 0)}
        self.main_measurement = self.measurements["None"]
        self.values = 11
        self.fps = 10
        self.timer = QtCore.QTimer()
        #self.start_timer()

        layout = QGridLayout()
        # {
        self.label = QLabel()
        layout.addWidget(self.label, 0, 1)

        settings = QVBoxLayout()
        # {
        qbox = QComboBox()
        qbox.addItems(["None", "Добавить среду..."])
        qbox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        settings.addWidget(qbox)

        create_dimension = QGridLayout()
        # {
        line_name = QLineEdit()
        line_name.setPlaceholderText("Name")
        line_d = QLineEdit()
        line_d.setPlaceholderText("Dimensions")
        button_create = QPushButton("Create")
        button_cancel = QPushButton("Cancel")
        create_dimension.addWidget(line_name, 0, 0)
        create_dimension.addWidget(line_d, 1, 0)
        create_dimension.addWidget(button_create, 2, 0)
        create_dimension.addWidget(button_cancel, 2, 1)
        # } create_dimension
        # settings.addLayout(create_dimension)
        # } settings
        layout.addLayout(settings, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        # } layout
        self.setCentralWidget(widget)
        self.draw_d(self.main_measurement)
        self.show()

    def draw_d(self, main_m):
        canvas = QPixmap(self.width, self.height)
        canvas.fill(QColor('white'))
        painter = QPainter(canvas)

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor('black'))
        painter.setPen(pen)

        font = QFont()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)

        if main_m.d == 1:
            division = self.values - 1
            division = self.side_size // division
            painter.drawLine(0, self.side_size // 2, self.side_size, self.side_size // 2)
            for i in range(self.values):
                painter.drawLine(i * division, self.side_size // 2, i * division, self.side_size // 2 + 10)
                painter.drawText(i * division - 3, self.side_size // 2 + 22, str((main_m.x + i) * main_m.scale))
            for i in main_m.objects:
                if main_m.x * main_m.scale <= i.x <= (main_m.x + self.values - 1) * main_m.scale:
                    painter.drawEllipse(self.calculate_x(i.x, division), self.side_size // 2 - 5, 10, 10)
        elif main_m.d == 2:
            division = (self.side_size - 30) // (self.values - 1)
            painter.drawLine(30, 0, 30, self.side_size - 30)
            painter.drawLine(30, self.side_size - 30, self.side_size, self.side_size - 30)
            for i in range(self.values):
                painter.drawLine(20, i * division, self.side_size, i * division)
                painter.drawText(0, self.side_size - 27 - i * division, str((main_m.y + i) * main_m.scale))
                painter.drawLine(30 + i * division, self.side_size - 30, 30 + i * division, 0)
                painter.drawText(i * division + 24, self.side_size - 8, str((main_m.x + i) * main_m.scale))
            for i in main_m.objects:
                if main_m.x * main_m.scale <= i.x <= (main_m.x + self.values - 1) * main_m.scale \
                        and main_m.y * main_m.scale <= i.y <= (main_m.y + self.values - 1) * main_m.scale:
                    painter.drawEllipse(self.calculate_x(i.x, division) + 30, self.calculate_y(i.y, division), 10, 10)
        painter.end()
        self.label.setPixmap(canvas)

    def start_timer(self):
        self.timer.timeout.connect(self.iteration)
        self.main_measurement.t = time.time()
        self.timer.start(int(1000 / self.fps))

    def iteration(self):
        t = time.time() - self.main_measurement.t
        for i in self.main_measurement.objects:
            i.time_sync(t)
        self.draw_d(self.main_measurement)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_A:
            self.main_measurement.x -= 1
        if event.key() == QtCore.Qt.Key.Key_D:
            self.main_measurement.x += 1
        if event.key() == QtCore.Qt.Key.Key_S:
            self.main_measurement.y -= 1
        if event.key() == QtCore.Qt.Key.Key_W:
            self.main_measurement.y += 1
        if event.key() == QtCore.Qt.Key.Key_Plus:
            self.main_measurement.scale *= 0.5
        if event.key() == QtCore.Qt.Key.Key_Minus:
            self.main_measurement.scale *= 2
        self.draw_d(self.main_measurement)

    def calculate_x(self, xo, division):
        return round((xo / self.main_measurement.scale - self.main_measurement.x) * division) - 5

    def calculate_y(self, yo, division):
        return self.side_size - round((yo / self.main_measurement.scale - self.main_measurement.y) * division) - 30 - 5


class Measurement():
    def __init__(self, d, x, y):
        self.d = d
        self.x = x
        self.y = y
        self.scale = 1
        self.objects = []
        self.t = 0


class Object():
    def __init__(self, x0, y0, v0, a0):
        self.x0 = x0
        self.y0 = y0
        self.v0 = Vector(v0)
        self.a0 = Vector(a0)
        self.v = self.v0.copy()
        self.x = self.x0
        self.y = self.y0

    def time_sync(self, t):
        self.x = self.x0 + self.v0.x * t + self.a0.x * t * t * 0.5
        self.y = self.y0 + self.v0.y * t + self.a0.y * t * t * 0.5
        self.v = self.v0 + self.a0 * t


class Vector():
    def __init__(self, vector):
        self.x = vector[0]
        self.y = vector[1]

    def copy(self):
        return Vector([self.x, self.y])

    def __add__(self, other):
        return Vector([self.x + other.x, self.y + other.y])

    def __mul__(self, other):
        return Vector([self.x * other, self.y * other])


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    app.exec()

'''
Поработать над перемещением в пространстве
Рвсстановка виджетов (сделать, чтоб окно не раздвигалось)
Сделать дополнительные линеечки
'''
