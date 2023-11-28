from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QStackedLayout, QWidget,
                             QLineEdit, QPushButton)
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen, QFont


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.side_size = 600
        self.measurements = {"None": Measurement(0, 0, 0, 1)}
        self.main_measurement = self.measurements["None"]
        self.values = 11

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
        elif main_m.d == 2:
            division = self.values - 1
            divisionx = (self.side_size - 30) // division
            divisiony = (self.side_size - 30) // division
            painter.drawLine(30, 0, 30, self.side_size - 30)
            painter.drawLine(30, self.side_size - 30, self.side_size, self.side_size - 30)
            for i in range(self.values):
                painter.drawLine(20, i * divisiony, self.side_size, i * divisiony)
                painter.drawText(0, self.side_size - 27 - i * divisiony, str((main_m.y + i) * main_m.scale))
                painter.drawLine(30 + i * divisionx, self.side_size - 30, 30 + i * divisionx, 0)
                painter.drawText(i * divisionx + 24, self.side_size - 8, str((main_m.x + i) * main_m.scale))

        painter.end()
        self.label.setPixmap(canvas)

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
            self.main_measurement.scale *= 2
        if event.key() == QtCore.Qt.Key.Key_Minus:
            self.main_measurement.scale *= 0.5
        self.draw_d(self.main_measurement)


class Measurement():
    def __init__(self, d, x, y, scale):
        self.d = d
        self.x = x
        self.y = y
        self.scale = scale


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    app.exec()

'''
Поработать над перемещением в пространстве
Рвсстановка виджетов (сделать, чтоб окно не раздвигалось)
Сделать дополнительные линеечки
'''
