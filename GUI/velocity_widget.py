from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg

class VelocityWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Setup Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create Label Widget
        self.velocity_label = QLabel("Velocity: Movement = 0")
        layout.addWidget(self.velocity_label)

        # Create PyQtGraph Widget
        self.velocity_plot_widget = pg.PlotWidget()
        self.velocity_plot_widget.setBackground('w') #sets the background to white for better readability
        layout.addWidget(self.velocity_plot_widget)


        # Grab the underlying PlotItem (for configuring axes, etc.)
        self.plot = self.velocity_plot_widget.getPlotItem()

        # Hide the X axis
        self.plot.showAxis('bottom', False)

        # Create bar for graph
        # x = [0] means our bas is positioned at x=0
        # height = [inital_value]
        # width controls thickness
        # brush sets color/fill
        self.bar_item = pg.BarGraphItem(x=[0], height=[0], width=0.1, brush='green')

        # if we wanted to create multiple bars instead of 1 bar, we can use a array
        # for example if we wanted 5 bars:
        # x_positions = [0, 1, 2, 3, 4, 5]
        # heights = [10, 40, 20, 80, 60]
        # self.bar_item = pg.BarGraphItem(x=x_positions, height=heights, width=0.8, brush='green')

        # Add the bar item to the plot
        self.plot.addItem(self.bar_item)

        # Lock the plot in place
        self.plot.enableAutoRange('xy', False) # Turn off auto-ranging
        self.plot.setRange(xRange = (-0.5, 0.5), yRange = (-1, 1)) # Lock the view to these ranges
        self.plot.setMouseEnabled(x=False, y=False) # Disable Zoom and pan


        
        # Add to layout
        layout.addWidget(self.velocity_plot_widget)

        # Inital bar height
        self.current_velocity = 0 

    def get_target_velocity(self, input):
        """
        Read data and update the bar's height accordingly.
        """
        y_max = 1023
        y_min = 0
        mid_point = y_max/2 
        

        # adding a "Dead Zone" so that if the joystick picks ups some noise it doesn't just start moving the motor
        buffer = 100
        lower_dead_zone = mid_point-buffer
        higher_dead_zone = mid_point+buffer

        # Calculate what the velocity whould be depending on the input
        if  input > higher_dead_zone:
            # positive ratio
            ratio = ((input - higher_dead_zone) / (y_max - higher_dead_zone))
            return 0.0 + ratio
        elif input < lower_dead_zone:
            # negative ratio
            ratio = ((input - y_min) / (lower_dead_zone - y_min))
            return -1.0 + ratio
        else:
            return 0.0

        # update axis range if desired
        # self.plot.setYRange(0, 100)

    def update_acceleration_input(self, input, dt=1.0/60.0):
        """
        Uses input to update internal velocity via acceleration logic, 
        then updates the bar and label to show new velocity. 
        """        
        
        # get target acceleration (targt velocity ratio)
        accel_input = (self.get_target_velocity(input) * -1)

        # factors
        accel_factor = 100.0 # Scale factor for how strongly we accelerate
        friction = 0.5     # friction or drag coefficient
        max_velocity = 1.0
        min_velocity = -1.0


        # Algorithm for acceleration (velocity += (acceleration * factor) * dt(dt is delta time))
        new_velocity = self.current_velocity + (accel_input * accel_factor) * dt
        
        # Apply friction: velocity -= friction * velocity * dt
        # (works for positive or negative velocity, since it scales velocity by a factor < 1)
        new_velocity = self.current_velocity - friction * new_velocity * dt        


        if new_velocity > max_velocity:
            new_velocity = max_velocity
        elif new_velocity < min_velocity:
            new_velocity = min_velocity

        self.current_velocity = new_velocity

        # Update the bar
        self.bar_item.setOpts(height=[self.current_velocity])
        
        # Update label (only show the first 2 decimals of float)
        self.velocity_label.setText(f"Velocity: Movement = {self.current_velocity:.2f}, Input = {accel_input}")

        # force a redraw
        self.update()
        



