from serial import Serial
import time

arduino_a = Serial('COM3', 9600) 
arduino_t = Serial('COM9', 9600) 
#Which arduino it connects to doesnt matter, as lnog as teh com ports are correctly seelcted for the two arduinos
jnt = "000"

time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
  jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")
   
  arduino_a.write(jnt.encode()) 
  arduino_t.write(jnt.encode()) 
  
  #print("Azimuth Angle  e" +arduino_a.readline().decode('utf') )
  #time.sleep(0.01)
  #print("Theta   Angle  " +arduino_t.readline().decode('utf'))
 
  #time.sleep(1)
    ################################# ###############

