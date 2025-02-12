import serial #handles serial communication
import json
import os 


SERIAL_PORT = "COM3"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) #Opens a serial connection with micro controller
                                                       #timeout=1 (if no data is recieved within 1 second, prevents freezing)

#Function to clear the terminal
def clear_screen():
    # on windows it runs cls, on linux or mac it runs clear
    os.system('cls' if os.name == 'nt' else 'clear')
    
while True:
    try:
        line = ser.readline().decode("utf-8").strip() #Read line from transitter
        if line:
            clear_screen()
            try:
                pressed = "none"
                data = json.loads(line)
                
                print(f"Joystick Data: X = {data['input']['js1']['X']}, Y = {data['input']['js1']['Y']}, SW = {data['input']['js1']['SW']}")
                print(f"Button Data: b1 = {data['input']['buttons']['b1']}")
                #print(f"ultrasonic Sensor Data: u1 = {data['outputs']['u1']}")
            except json.JSONDecodeError:
                print("Recieved malformed data: ", line)
                
    except KeyboardInterrupt:
        print("\n❌ Exiting...")
        break



