from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen, QFont


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.side_size = 600
        self.d = 2
        self.camera_x = 0
        self.camera_y = 0
        self.values = 11
        self.scale = 1.0
        layout = QGridLayout()
        #{
        self.label = QLabel()
        layout.addWidget(self.label, 0, 1)

        settings = QVBoxLayout()
        #{
        qbox = QComboBox()
        qbox.setEditable(True)
        qbox.addItems(["None", "Добавить среду..."])
        settings.addWidget(qbox)

        create_dimension = QGridLayout()
        #{
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
        #} create_dimension
        settings.addLayout(create_dimension)

        #} settings
        layout.addLayout(settings, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        #} layout
        self.setCentralWidget(widget)
        self.draw_d()
        self.show()


    def draw_d(self):
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


        if self.d == 1:
            division = self.values - 1
            division = self.side_size // division
            painter.drawLine(0, self.side_size // 2, self.side_size, self.side_size // 2)
            for i in range(self.values):
                painter.drawLine(i * division, self.side_size // 2, i * division, self.side_size // 2 + 10)
                painter.drawText(i * division - 3, self.side_size // 2 + 22, str((self.camera_x + i) * self.scale))
        elif self.d == 2:
            division = self.values - 1
            divisionx = (self.side_size - 30) // division
            divisiony = (self.side_size - 30) // division
            painter.drawLine(30, 0, 30, self.side_size - 30)
            painter.drawLine(30, self.side_size - 30, self.side_size, self.side_size - 30)
            for i in range(self.values):
                painter.drawLine(20, i * divisiony, self.side_size, i * divisiony)
                painter.drawText(0, self.side_size - 27 - i * divisiony, str((self.camera_y + i) * self.scale))
                painter.drawLine(30 + i * divisionx, self.side_size - 30, 30 + i * divisionx, 0)
                painter.drawText(i * divisionx + 24, self.side_size - 8, str((self.camera_x + i) * self.scale))

        painter.end()
        self.label.setPixmap(canvas)



    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.camera_x -= 1
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.camera_x += 1
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.camera_y -= 1
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.camera_y += 1
        if event.key() == QtCore.Qt.Key.Key_Plus:
            self.scale *= 2
        if event.key() == QtCore.Qt.Key.Key_Minus:
            self.scale *= 0.5
        self.draw_d()


class Measurement():
    def __init__(self, d, x, y):
        self.d = d
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
