import serial
import time

arduino_n = serial.Serial('/dev/ttyACM1', 9600) # Replace 'COM3' with the appropriate serial port on your computer
arduino_l = serial.Serial('/dev/ttyACM2', 9600) # Replace 'COM3' with the appropriate serial port on your computer


time.sleep(2) # Give some time for the serial connection to establish

while(True):
    val = input("Enter angle value for azimuth")
    arduino_n.write(val.encode()) 
    val = input("Enter angle value for theta")
    arduino_l.write(val.encode()) 

56
