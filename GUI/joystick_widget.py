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
        self.timer.start(100)

    def update_data(self):
        """Reads joystick data from serial and update graph"""
        data = read_serial()
        if data:
            try: 
                x_pos = data["input"]["js1"]["X"]
                y_pos = data["input"]["js1"]["Y"]
                sw = data["input"]["js1"]["SW"]
                self.joystick_dot.setData([x_pos], [y_pos])
                self.joystick_label.setText(f"Joystick: X = {x_pos}, Y = {y_pos}, SW = {sw}")
            except KeyError:
                pass #ignore missing data fields
    