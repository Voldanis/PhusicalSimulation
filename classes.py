from PyQt5.QtGui import QPainter, QPixmap


class Object:
    def simulate(self, t: float):
        raise NotImplementedError
    
    def top_left_corner(self) -> (float, float):
        raise NotImplementedError

    def draw(self, painter: QPainter, unit: int, offset: int, canvas: QPixmap,
             measure: 'Measurement'):
        raise NotImplementedError


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

    def simulate(self, t: float):
        dt = t - self.last_sim
        self.x += self.velocity.x * dt + self.acceleration * dt * dt / 2
        self.y += self.velocity.y * dt + self.acceleration.y * dt * dt / 2
        self.velocity += self.acceleration * dt
    
    def top_left_corner(self, unit: int, offset: int, canvas: QPixmap,
                        measure: 'Measurement'):
        if measure.dimensions_num == 1:
            return (self.x*unit - self.radius//2 - measure.cam_x*unit + offset,
                    canvas.height()//2 - self.radius//2)
        else:
            return (self.x*unit - self.radius//2 - measure.cam_x*unit + offset,
                    canvas.height() - self.y*unit - self.radius//2 + measure.cam_y*unit - offset)
    
    def draw(self, painter: QPainter, unit: int, offset: int, canvas: QPixmap,
             measure: 'Measurement'):
        painter.drawEllipse(*self.top_left_corner(unit, offset, canvas, measure),
                            self.radius, self.radius)


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
