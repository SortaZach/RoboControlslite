import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from joystick_widget import JoystickWidget
from buttons_widget import ButtonWidget

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

        # Add Widgets to Layout
        self.joystick_widget = JoystickWidget()
        self.button_widget = ButtonWidget()

        # Add Widgets to layout with positions
        layout.addWidget(self.joystick_widget, 0, 0)
        layout.addWidget(self.button_widget, 0, 1)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainDashboard()
    window.show()
    sys.exit(app.exec())




    