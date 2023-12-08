from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget


class Object:
    info_content: list[tuple[str, str] | str]

    def simulate(self, t: float):
        raise NotImplementedError
    
    def top_left_corner(self) -> (float, float):
        raise NotImplementedError

    def draw(self, painter: QPainter, unit: int, offset: int, canvas_h: int,
             measure: 'Measurement'):
        raise NotImplementedError

    def is_contain_point(self, x: int, y: int, fault: int, unit: int, offset: int,
                         canvas_h: int, measure: 'Measurement') -> bool:
        raise NotImplementedError
    
    def get_info_widget(self) -> QWidget:
        if not hasattr(self, "info_content"):
            raise NotImplementedError("self.info_content must be implemented")

        widget = QWidget()
        layout = QGridLayout(widget)
        for i, row in enumerate(self.info_content):
            if isinstance(row, str):
                layout.addWidget(QLabel(row), i, 0)
            else:
                layout.addWidget(QLabel(row[0]), i, 0)
                layout.addWidget(QLabel(row[1]), i, 1, Qt.AlignmentFlag.AlignRight)
        return widget


class Point(Object):
    def __init__(self, x: float, y: float, radius: float,
                 vx: float, vy: float,
                 ax: float, ay: float, created_time: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = Vector(vx, vy)
        self.acceleration = Vector(ax, ay)
        self.last_sim = created_time
        self.info_content = [
            "Точка",
            ("X", f"{self.x}"), ("Y", f"{self.y}")
        ]

    def simulate(self, dt: float):
        """
        Args:
            dt (float): time delta
        """
        self.x += self.velocity.x * dt + self.acceleration.x * dt * dt / 2
        self.y += self.velocity.y * dt + self.acceleration.y * dt * dt / 2
        self.velocity += self.acceleration * dt
    
    def center(self, unit: int, offset: int, canvas_h: int, measure: 'Measurement'):
        if measure.dimensions_num == 1:
            return (round(self.x*unit - measure.cam_x*unit + offset),
                    canvas_h//2)
        else:
            return (round(self.x*unit - measure.cam_x*unit + offset),
                    round(canvas_h - self.y*unit
                          + measure.cam_y*unit - offset))
    
    def top_left_corner(self, unit: int, offset: int, canvas_h: int,
                        measure: 'Measurement'):
        return map(lambda coord: coord - self.radius//2,
                   self.center(unit, offset, canvas_h, measure))
    
    def draw(self, painter: QPainter, unit: int, offset: int, canvas_h: int,
             measure: 'Measurement'):
        painter.drawEllipse(*self.top_left_corner(unit, offset, canvas_h, measure),
                            self.radius, self.radius)
    
    def is_contain_point(self, x: int, y: int, fault: int, unit: int, offset: int,
                         canvas_h: int, measure: 'Measurement') -> bool:
        px, py = self.center(unit, offset, canvas_h, measure)
        return abs(px-x) <= fault and abs(py-y) <= fault


class Measurement:
    def __init__(self, dimensions_num, cam_x, cam_y):
        self.dimensions_num = dimensions_num
        self.cam_x = cam_x
        self.cam_y = cam_y
        self.scale = 1
        self.objects: list[Object] = []
        self.time = 0


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vector(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported sum")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError("Vector can be multiplied by int or float only")
