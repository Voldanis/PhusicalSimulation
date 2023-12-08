from math import ceil

from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QHideEvent, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from physic_models import Measurement


class ObjectInfo(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self):
        QVBoxLayout(self).setContentsMargins(0, 0, 0, 0)
        self.widget = None
        self.setWindowFlag(
            QtCore.Qt.WindowType.Popup
        )
    
    def setWidget(self, a0: QWidget):
        self.widget = a0
        self.layout().addWidget(a0)

    def hideEvent(self, a0: QHideEvent | None):
        self.layout().removeWidget(self.widget)
        self.widget = None


class Canvas(QLabel):
    def __init__(self, w: int, h: int, units_num: int, cur_maesure: Measurement):
        super().__init__()

        self.w = w
        self.h = h
        self.values = units_num
        self.cur_measure = cur_maesure

        self.init_ui()
    
    def init_ui(self):
        self.offset = 15
        self.object_info = ObjectInfo()
        self.setScaledContents(True)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev: QMouseEvent):
        if self.object_info.isVisible():
            return
        unit = ceil((self.width() - 30) // (self.values - 1) * self.cur_measure.scale)
        mouse_pos = ev.pos()
        for obj in self.cur_measure.objects:
            if obj.is_contain_point(mouse_pos.x(), mouse_pos.y(), 8, unit,
                                    self.offset, self.h, self.cur_measure):
                self.object_info.setWidget(obj.get_info_widget())
                self.object_info.move(ev.globalPos())
                self.object_info.show()
    
    def mousePressEvent(self, ev: QMouseEvent | None):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            unit = ceil((self.width() - 30) // (self.values - 1) * self.cur_measure.scale)
            mouse_pos = ev.pos()
            for obj in self.cur_measure.objects:
                if obj.is_contain_point(mouse_pos.x(), mouse_pos.y(), 5, unit,
                                        self.offset, self.h, self.cur_measure):
                    self.cur_measure.objects.remove(obj)
            self.draw_measurement(self.cur_measure)

    def draw_measurement(self, measure: 'Measurement'):
        self.cur_measure = measure

        pixmap = QPixmap(self.w, self.h)

        pixmap.fill(QColor("white"))
        painter = QPainter(pixmap)
        painter.setBrush(QtCore.Qt.GlobalColor.black)
        
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor("black"))
        painter.setPen(pen)

        font = QFont()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)

        offset = self.offset
        unit = ceil((pixmap.width() - 2*offset) // (self.values - 1) * measure.scale)
        if measure.dimensions_num == 1:
            painter.drawLine(0, pixmap.height() // 2,
                             pixmap.width(), pixmap.height() // 2)
            for i in range(ceil(pixmap.width() / unit)):
                painter.drawLine(i * unit + offset, pixmap.height() // 2,
                                 i * unit + offset, pixmap.height() // 2 + 10)
                painter.drawText(i * unit + offset - 3, pixmap.height() // 2 + 22,
                                 str(measure.cam_x + i))
        elif measure.dimensions_num == 2:
            painter.drawLine(-measure.cam_x * unit + offset, 0,
                             -measure.cam_x * unit + offset, pixmap.height())  # Vertical
            painter.drawLine(0, pixmap.height() + measure.cam_y * unit - offset,
                             pixmap.width(), pixmap.height() + measure.cam_y * unit - offset)  # Horizontal
            painter.setPen(QtCore.Qt.PenStyle.DotLine)
            for i in range(ceil(pixmap.width() / unit)):  # Dotted lines
                # Horizontal
                painter.drawLine(0, pixmap.height()-offset - i * unit,
                                 pixmap.width(), pixmap.height()-offset - i * unit)
                painter.drawText(0, pixmap.height()-offset - i * unit, str(measure.cam_y + i))
                # Vertical
                painter.drawLine(i * unit + offset, 0,
                                 i * unit + offset, pixmap.height())
                painter.drawText(i * unit + offset+2, pixmap.height()-2, str(measure.cam_x + i))
            painter.setPen(QtCore.Qt.PenStyle.SolidLine)

        for obj in measure.objects:
            obj.draw(painter, unit, offset, pixmap.height(), measure)

        painter.end()

        self.setPixmap(pixmap)
