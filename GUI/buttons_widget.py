from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from serial_reader import read_serial

class ButtonWidget(QWidget):
    def __init__(self):
        super().__init__()
    
        # Setup Layout
        layout = QVBoxLayout()
        self.setLayout(layout)


        # Create Label Widget
        self.button_label = QLabel("Buttons: b1 = 0")
        layout.addWidget(self.button_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def update_data(self):
        """Read button data from serial to update values"""
        data = read_serial()
        if data:
            try:
                b1 = data["input"]["buttons"]["b1"]
                self.button_label.setText(f"Buttons: b1 = {b1}")
            except KeyError:
                pass