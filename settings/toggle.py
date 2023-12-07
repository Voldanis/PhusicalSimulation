from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget


class ToggleSettings(QWidget):
    def __init__(self, measures_widget: QWidget, objects_widget: QWidget) -> None:
        super().__init__()

        self.measures_widget = measures_widget
        self.objects_widget = objects_widget
        objects_widget.hide()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.measures_button = QPushButton("Среды")
        self.measures_button.setCheckable(True)
        self.measures_button.setChecked(True)
        self.measures_button.clicked.connect(self.measures_clicked)
        self.objects_button = QPushButton("Объекты")
        self.objects_button.setCheckable(True)
        self.objects_button.clicked.connect(self.objects_clicked)

        layout.addWidget(self.measures_button)
        layout.addWidget(self.objects_button)
    
    def measures_clicked(self):
        if not self.measures_button.isChecked():
            self.measures_button.setChecked(True)
            return
        self.objects_button.setChecked(False)
        self.objects_widget.hide()
        self.measures_widget.show()
    
    def objects_clicked(self):
        if not self.objects_button.isChecked():
            self.objects_button.setChecked(True)
            return
        self.measures_button.setChecked(False)
        self.measures_widget.hide()
        self.objects_widget.show()
