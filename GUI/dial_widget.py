from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from serial_reader import read_serial

class DialWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.dial_label = QLabel("No Position...")
