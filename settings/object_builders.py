from time import time

from PyQt5.QtWidgets import QLineEdit, QMessageBox, QVBoxLayout, QWidget

from physic_models import Object, Point


class Builder:
    def get_widget(self) -> QWidget:
        raise NotImplementedError

    def is_valid(self, warning_parent: QWidget) -> bool:
        raise NotImplementedError

    def get_object(self) -> Object:
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class PointBuilder(Builder):
    def __init__(self):
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.x = QLineEdit()
        self.x.setPlaceholderText("X")
        self.y = QLineEdit()
        self.y.setPlaceholderText("Y")
        self.vx = QLineEdit()
        self.vx.setPlaceholderText("Vx")
        self.vy = QLineEdit()
        self.vy.setPlaceholderText("Vy")
        self.ax = QLineEdit()
        self.ax.setPlaceholderText("Ax")
        self.ay = QLineEdit()
        self.ay.setPlaceholderText("Ay")

        for widget in (self.x, self.y, self.vx, self.vy, self.ax, self.ay):
            layout.addWidget(widget)
    
    def get_widget(self):
        return self.widget
    
    def is_valid(self, warning_parent: QWidget) -> bool:
        if any(
            not widget.text().removeprefix('-').replace('.', '', 1).isdigit()
            for widget in (self.x, self.y, self.vx, self.vy, self.ax, self.ay)
        ):
            QMessageBox.warning(warning_parent, "Ошибка",
                                "Все поля должны быть рациональными числами.\n"
                                "Используйте \".\" для разделения")
            return False
        return True

    def get_object(self):
        return Point(
            *(
                float(item.text()) if isinstance(item, QWidget) else item for item in (
                    self.x, self.y, 10,
                    self.vx, self.vy, self.ax, self.ay
                )
            ),
            time()
        )
    
    def clear(self):
        for widget in (self.x, self.y,
                       self.vx, self.vy, self.ax, self.ay):
            widget.clear()
