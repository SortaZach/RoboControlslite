import json
import serial


SERIAL_PORT = "COM3"  # Change if necessary
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 

def read_serial():
    """Reads a line from the serial port and parses JSON"""
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        try:
            return json.loads(line)
        except (json.JSONDecodeError, KeyError):
            print("Received malformed data: ", line)
            return None
    return None