import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class SensorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sensor/Input Data Display")
        self.setGeometry(100, 100, 400, 200)  # Window position & size
        
        # Layout
        layout = QVBoxLayout()

        # Labels to display sensor data
        self.joystick_label = QLabel("Joystick: X = 0, Y = 0")
        self.button_label = QLabel("Button Pressed: None")

        # Add labels to layout
        layout.addWidget(self.joystick_label)
        layout.addWidget(self.button_label)

        self.setLayout(layout)

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SensorGUI()
    gui.show()
    sys.exit(app.exec())