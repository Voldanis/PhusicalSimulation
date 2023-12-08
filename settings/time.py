from typing import Callable

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget


class TimeSettings(QWidget):
    def __init__(self, start_callback: Callable[..., None],
                 stop_callback: Callable[..., None]) -> None:
        super().__init__()

        self.start_timer = start_callback
        self.stop_timer = stop_callback

        self.init_ui()
    
    def init_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.start_button = QPushButton("Пуск")
        self.start_button.clicked.connect(self.start_clicked)

        layout.addWidget(self.start_button, 1, 0, 1, 2)

    def start_clicked(self):
        if self.start_button.text() == "Пуск":
            self.start_timer()
            self.start_button.setText("Пауза")
        else:
            self.stop_timer()
            self.start_button.setText("Пуск")
