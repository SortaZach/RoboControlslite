from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from serial_reader import read_serial

class DialWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.dial_label = QLabel("No Position...")
        layout.addWidget(self.dial_label)

    def get_current_dial_position(self):
        d1 = "No reading..."
        data = read_serial()
        if data:
            d1 = data['input']['dials']['d1']
            sw = data['input']['dials']['SW']
            self.dial_label.setText(f"dial position: {d1}, SW: {sw}")
