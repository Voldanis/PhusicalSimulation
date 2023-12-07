from typing import Callable

from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from classes import Measurement
from utils import Pointer

from .object_builders import Builder, PointBuilder


class ObjectsSettings(QWidget):
    def __init__(self,
                 main_widget: QWidget,
                 cur_measurement: Pointer[Measurement],
                 draw_measurement: Callable[[Measurement], None]) -> None:
        super().__init__()
        self.builder: dict[str, Builder] = {"Точка": PointBuilder()}

        self.main_widget = main_widget
        self.cur_measurement = cur_measurement
        self.draw_measurement = draw_measurement

        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        self.type_box = QComboBox()
        self.type_box.addItems(self.builder.keys())
        self.type_box.activated[str].connect(self.changed_type)

        layout.addWidget(self.type_box)

        for builder in self.builder.values():
            layout.addWidget(builder.get_widget())
            builder.get_widget().hide()

        self.cur_type_widget = self.builder[self.type_box.currentText()].get_widget()
        self.cur_type_widget.show()

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_object)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_creating)

        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)
    
    def changed_type(self, text: str):
        self.cur_type_widget.hide()

        new_type_builder = self.builder[text]
        new_type_builder.clear()

        new_type_builder.get_widget().show()
        self.cur_type_widget = new_type_builder.get_widget()
    
    def create_object(self):
        builder = self.builder[self.type_box.currentText()]
        if builder.is_valid(self.main_widget):
            new_object = builder.get_object()
            (+self.cur_measurement).objects.append(new_object)
        self.draw_measurement(+self.cur_measurement)
    
    def cancel_creating(self):
        self.builder[self.type_box.currentText()].clear()
