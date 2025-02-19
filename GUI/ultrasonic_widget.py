from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from serial_reader import read_serial

class UltrasonicWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.sonic_label = QLabel("Nothing in sensor range...")
        layout.addWidget(self.sonic_label)


    def update_reading(self):
        u1 = "No reading..."
        data = read_serial()
        if data:
            u1 = data['outputs']['u1']
            if u1 == 9999:
                self.sonic_label.setText("No object in Radars Range...")
            elif u1 < 10: 
                self.sonic_label.setText("TOO CLOSE!!!!")
            else:
                self.sonic_label.setText(f"Current distance to closest object is {u1}cm")
            
        self.update()
