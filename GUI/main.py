import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt6.QtCore import QTimer
from joystick_widget import JoystickWidget
from buttons_widget import ButtonWidget
from velocity_widget import VelocityWidget
from ultrasonic_widget import UltrasonicWidget

class mainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dyforge Dashboard")
        self.setGeometry(100, 100, 800, 400)
        
        # Create Centreal Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Add Widgets
        self.joystick_widget = JoystickWidget()
        self.button_widget = ButtonWidget()
        self.velocity_widget = VelocityWidget()
        self.ultrasonic_widget = UltrasonicWidget()

        # Add Widgets to layout with positions
        layout.addWidget(self.ultrasonic_widget, 0, 0)
        layout.addWidget(self.joystick_widget, 1, 0)
        # layout.addWidget(self.button_widget, 0, 1) # Currently no buttons set up
        layout.addWidget(self.velocity_widget, 1, 1)


        #Timer For data updates (also so we dont get a ton of repetative input)
        self.timer = QTimer()
        self.timer.timeout.connect(self.joystick_widget.update_data)
        self.timer.timeout.connect(self.ultrasonic_widget.update_reading)
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(16) # 60fps
        self.last_time = time.time() # Track last udate time

    def update_dashboard(self):
        # figure how much time has passed since last frame
        now = time.time() 
        dt = now - self.last_time
        self.last_time = now
        
        joystick_x, joystick_y, joystick_sw = self.joystick_widget.get_current_joystick_data()
        self.velocity_widget.update_acceleration_input(joystick_x, dt=dt)
        return
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainDashboard()
    window.show()
    sys.exit(app.exec())




    