from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QStackedLayout, QWidget,
                             QLineEdit, QPushButton)
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen, QFont


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.side_size = 600
        self.measurements = {"None": Measurement(2, 0, 0)}
        self.main_measurement = self.measurements["None"]
        self.main_measurement.objects.append(Object(1, 1))
        self.values = 11
        '''self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerr)
        self.timer.start(1000)'''


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
        canvas = QPixmap(self.side_size, self.side_size)
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
                    #print(self.calculate_x(i.x, main_m.x, division), )
        painter.end()
        self.label.setPixmap(canvas)

    def timerr(self):
        print(1)

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
            self.main_measurement.x += 5 * self.main_measurement.scale
        if event.key() == QtCore.Qt.Key.Key_Minus:
            '''self.main_measurement.x *= self.main_measurement.scale
            self.main_measurement -= 5 * self.main_measurement.scale
            self.main_measurement.x /= self.main_measurement.scale
            print(1)'''
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
        self.scale = 4
        self.objects = []


class Object():
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    app.exec()

'''
Поработать над перемещением в пространстве
Рвсстановка виджетов (сделать, чтоб окно не раздвигалось)
Сделать дополнительные линеечки
'''
