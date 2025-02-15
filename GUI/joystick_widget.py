from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from serial_reader import read_serial

class JoystickWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Setup Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create Label Widget
        self.joystick_label = QLabel("Joystick: X = 0, Y = 0, SW = 0")
        layout.addWidget(self.joystick_label)

        # Create PyQtGraph Widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)


        # Setup Graph Limits
        self.plot_widget.setXRange(0, 1023)
        self.plot_widget.setYRange(0, 1023)
        self.plot_widget.setLabel("left", "Y Position")
        self.plot_widget.setLabel("bottom", "X Position" )

        # Create Moving Point For Joystick
        self.joystick_dot = self.plot_widget.plot([], [], pen=None, symbol="o", symbolBrush="r")

        #Timer For Updating
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(20)

        #Initialize the joysticks "current" position
        self.current_x = 500 # 500 is roughly middle value
        self.current_y = 500

    def update_data(self):
        """Reads joystick data from serial and update graph"""
        data = read_serial()
        if data:
            try: 
                x_pos = data["input"]["js1"]["X"]
                y_pos = data["input"]["js1"]["Y"]
                sw = data["input"]["js1"]["SW"]
                self.updateJoystick(x_pos, y_pos, sw)
            except KeyError:
                pass #ignore missing data fields
    

    def updateJoystick(self, new_x=None, new_y=None, sw=None):
        # we will use LERP (Linear interpolation) to smooth the readings of the joystick
        # LERPs equation: new_value = current_value * (1 - alpha) + target_value * alpha
        # alpha is a double between 0 and 1, current value is the value the sick is at
        # the target value is the value the stick is "jumping" to
        alpha = 0.3
        self.current_x = self.current_x * (1 - alpha) + new_x * alpha
        self.current_y = self.current_y * (1 - alpha) + new_y * alpha

        self.joystick_dot.setData([self.current_x], [self.current_y])
        self.joystick_label.setText(f"Joystick: X = {self.current_x}, Y = {self.current_y}, SW = {sw}")       
        self.update()