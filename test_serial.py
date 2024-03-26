import serial
import time

arduino_a = serial.Serial('/dev/ttyACM1', 9600) 
arduino_t = serial.Serial('/dev/ttyACM0', 9600) 
jnt = "000"

time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
  jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")
   
  arduino_a.write(jnt.encode()) 
  arduino_t.write(jnt.encode()) 
    ################################################


    
    
    

    
    

