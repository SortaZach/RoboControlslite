import sys
import json
import serial
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import QTimer

SERIAL_PORT = "COM3"  # Change if necessary
BAUD_RATE = 9600

class SensorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensor_data)
        self.timer.start(100)  # Update every 100ms

    def initUI(self):
        self.setWindowTitle("Sensor Data Display")
        self.setGeometry(100, 100, 400, 300)
        
        # Layout
        layout = QVBoxLayout()

        # Labels
        self.joystick_label = QLabel("Joystick: X = 0, Y = 0")
        self.button_label = QLabel("Button Pressed: None")
        #self.ultrasonic_label = QLabel("Ultrasonic Distance: N/A")

        # Debug output box
        self.debug_output = QTextEdit()
        self.debug_output.setReadOnly(True)


        # Add to layout
        layout.addWidget(self.joystick_label)
        layout.addWidget(self.button_label)
        #layout.addWidget(self.ultrasonic_label)
        layout.addWidget(self.debug_output)

        self.setLayout(layout)

    def update_sensor_data(self):
        try:
            line = self.ser.readline().decode("utf-8").strip()
            if line:
                data = json.loads(line)

                # Update labels with new sensor values
                self.joystick_label.setText(f"Joystick: X = {data['input']['js1']['X']}, Y = {data['input']['js1']['Y']}")
                self.button_label.setText(f"Button Pressed: {data['input']['buttons']['b1']}")
                #self.ultrasonic_label.setText(f"Ultrasonic Distance: {data['outputs'].get('u1', 'N/A')} cm")

                # Add raw data to debug output
                self.debug_output.append(line)
        except (json.JSONDecodeError, KeyError) as e:
            self.debug_output.append(f"Malformed data: {line} ({e})")

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SensorGUI()
    gui.show()
    sys.exit(app.exec())