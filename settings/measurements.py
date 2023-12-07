from typing import Callable

from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from classes import Measurement
from utils import Pointer


class MeasurementsSettings(QWidget):
    def __init__(self, measurements: dict[str, Measurement],
                 cur_measurement: Pointer,
                 draw_measurement: Callable[[Measurement], None]) -> None:
        super().__init__()

        self.measurements = measurements
        self.cur_measurement = cur_measurement
        self.draw_measurement = draw_measurement

        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        self.measure_box = QComboBox()
        self.measure_box.addItems(self.measurements.keys())
        self.measure_box.activated[str].connect(self.measure_box_changed)
        layout.addWidget(self.measure_box)        

        self.create_measure = QWidget()
        create_measure = QGridLayout(self.create_measure)
        create_measure.setContentsMargins(0, 0, 0, 0)

        self.measure_name = QLineEdit()
        self.measure_name.setPlaceholderText("Name")
        self.measure_dims_num = QLineEdit()
        self.measure_dims_num.setPlaceholderText("Dimensions")
        button_create = QPushButton("Create")
        button_create.clicked.connect(self.measurement_create)
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.measurement_cancel)

        create_measure.addWidget(self.measure_name, 0, 0, 1, 2)
        create_measure.addWidget(self.measure_dims_num, 1, 0, 1, 2)
        create_measure.addWidget(button_create, 2, 0)
        create_measure.addWidget(button_cancel, 2, 1)

        layout.addWidget(self.create_measure)
    
        layout.addStretch()

        delete_measure = QPushButton("Удалить среду")
        self.delete_measure_verify_window: QWidget | None = None
        delete_measure.clicked.connect(self.delete_measure_verify)
        layout.addWidget(delete_measure)

        self.vars_box = QWidget()
        vars_layout = QGridLayout(self.vars_box)
        vars_layout.setContentsMargins(0, 0, 0, 0)

        self.cur_g = 0
        vars_layout.addWidget(QLabel("g"), 0, 0)
        self.var_g = QLineEdit()
        self.var_g.setPlaceholderText("Рац g. Через \".\"")
        self.var_g.setText('0')
        self.var_g.editingFinished.connect(self.var_g_changed)

        vars_layout.addWidget(self.var_g, 0, 1)
        layout.addWidget(self.vars_box)
    
    def measure_box_changed(self, text: str):
        measurement = self.measurements.get(text)
        if measurement is None:
            return
        self.cur_measurement << measurement
        self.draw_measurement(measurement)
    
    def measurement_create(self):
        measure_name = self.measure_name.text()
        if self.measure_dims_num.text() not in ('1', '2'):
            self.measure_dims_num.setPlaceholderText("Только 1 или 2")
            self.measure_dims_num.setText('')
            return
        if measure_name in self.measurements:
            self.measure_name.setPlaceholderText(f"Имя {measure_name} занято")
            self.measure_name.setText('')
            return

        dims_num = int(self.measure_dims_num.text())
        self.measurements[measure_name] = Measurement(dims_num, 0, 0)
        self.measure_box.addItem(measure_name)

        self.measurement_cancel()

    def measurement_cancel(self):
        self.measure_name.setText('')
        self.measure_name.setPlaceholderText("Name")
        self.measure_dims_num.setText('')
        self.measure_dims_num.setPlaceholderText("Dimensions")
    
    def delete_measure_verify(self):
        if len(self.measurements) == 1:
            QMessageBox.warning(self, "Не возможно", "Осталось только одно измерение")
            return

        if not self.delete_measure_verify_window:
            window = QWidget()
            window.setWindowTitle("Удаление")

            layout = QGridLayout(window)
            layout.addWidget(QLabel("Подтвердите удаление текущего измерения"), 0, 0, 1, 2)

            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(self.delete_measure)
            cancel_button = QPushButton("Отмена")
            cancel_button.clicked.connect(self.cancel_deleting)

            layout.addWidget(delete_button, 1, 0)
            layout.addWidget(cancel_button, 1, 1)

            self.delete_measure_verify_window = window

        self.delete_measure_verify_window.show()

    def delete_measure(self):
        for k, v in self.measurements.items():
            if v is +self.cur_measurement:
                self.measurements.pop(k)
                for i in range(self.measure_box.count()):
                    if self.measure_box.itemText(i) == k:
                        self.measure_box.removeItem(i)
                break

        item = next(iter(self.measurements.items()))
        name = item[0]
        self.cur_measurement << item[1]

        self.draw_measurement(+self.cur_measurement)
        self.measure_box.setCurrentText(name)
        self.delete_measure_verify_window.hide()

    def cancel_deleting(self):
        self.delete_measure_verify_window.hide()
    
    def var_g_changed(self):
        if not self.var_g.text().replace('.', '', 1).isdigit():
            self.var_g.setText('')
            return
        
        self.cur_g = float(self.var_g.text())
