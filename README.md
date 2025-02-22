# Robolite
 
Robolite is an educational project designed to interface with the ATmega328p on an Arduino Uno. It showcases the integration of various inputs and outputs—such as sensors, buttons, and encoders—to help users gain a deeper understanding of microcontroller capabilities and embedded system design.

With a graphical user interface (GUI) built using PyQt6, Robolite displays real-time data from the Arduino, while also providing a terminal output for debugging and detailed logging. The system offers a hands-on learning environment for working with AVR standards and experimenting with various hardware components.

** Features **

    - Microcontroller Integration:
        Interact with an ATmega328p via an Arduino Uno.

    - Real-Time Data Acquisition:
        Read and display sensor data, encoder values, and other inputs in real time.

    - Graphical User Interface:
        Utilize PyQt6 for a responsive, modern GUI that visualizes data and system status.

    - Serial Communication:
        Use pyserial to reliably transfer data between the Arduino and the host computer.

    - Data Visualization:
        Graphical display of sensor data and system outputs using pyqtgraph.


** Requirements **
Before you begin, ensure you have the following installed:

Python Packages:

    - PyQt6 – for building the GUI.
    - pyqtgraph – for data visualization and graphing.
    - pyserial – for serial communication with the Arduino.

Hardware:
    - Arduino Uno with ATmega328p.
    - Various sensors and input devices (joystick, rotary encoder, ultrasonic sensor, etc.).