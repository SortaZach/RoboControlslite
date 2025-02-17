from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
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
        self.plot_widget.setLabel("left", "X Position")
        self.plot_widget.setLabel("bottom", "Y Position" )

        # Create Moving Point For Joystick
        self.joystick_dot = self.plot_widget.plot([], [], pen=None, symbol="o", symbolBrush="r")

        #Initialize the joysticks "current" position
        self.current_x = 500 # 500 is roughly middle value
        self.current_y = 500
        self.sw = 0

    def update_data(self):
        """Reads joystick data from serial and update graph"""
        data = read_serial()
        if data:
            try: 
                self.current_x = data["input"]["js1"]["X"]
                self.current_y = data["input"]["js1"]["Y"]
                self.sw = data["input"]["js1"]["SW"]
                self.updateJoystick(self.current_x, self.current_y, self.sw)
            except KeyError:
                pass #ignore missing data fields
    

    def updateJoystick(self, new_x=None, new_y=None, sw=None):
        # call update function to make sure we're geting current values
        # we will use LERP (Linear interpolation) to smooth the readings of the joystick
        # LERPs equation: new_value = current_value * (1 - alpha) + target_value * alpha
        # alpha is a double between 0 and 1, current value is the value the sick is at
        # the target value is the value the stick is "jumping" to
        #alpha = 0.3

        #self.current_x = self.current_x * (1 - alpha) + new_x * alpha
        #self.current_y = self.current_y * (1 - alpha) + new_y * alpha
        
        #use raw data instead
        self.current_x = new_x
        self.current_y = new_y
        self.sw = sw

        self.joystick_dot.setData([self.current_y], [self.current_x])
        self.joystick_label.setText(f"Joystick: X = {self.current_x}, Y = {self.current_y}, SW = {sw}")       
        
        self.update()
        # This will be the raw data reading, so it'll still be a little choppy. 
        # We'll use a different widget to showcase the readings for velocity (acceleration/deceleration)
        # Which will be a much smoother transition then Just using LERP or raw data.

    def get_current_joystick_data(self):
        return self.current_x, self.current_y, self.sw