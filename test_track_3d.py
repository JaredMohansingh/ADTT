import serial
import time
from laser_aimer import find_az_and_theta

arduino_a = serial.Serial('/dev/ttyACM1', 9600) 
arduino_t = serial.Serial('/dev/ttyACM0', 9600) 
jnt = "000"

laser_posn =  [ 2, -1.9, 2.3 ]


time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
  jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")
  if (jnt == "x"):
    break
  arduino_a.write(jnt.encode()) 
  arduino_t.write(jnt.encode()) 
    ################################# ###############


while (True):
  x=0
  y=0
  z=0
  x = input("ENter x value")
  y = input("ENter y value")
  z = input("Enter z value")

  target_posn = [float(x),float(y),float(z)]

  az,theta = find_az_and_theta(laser_posn, target_posn)
  #print(az)
  #print(theta)


  command = "t" + str(theta) + "\r"
  print(command)
  arduino_a.write(command.encode()) 
  arduino_t.write(command.encode())

  command = "a" + str(az) + "\r"
  print(command)
  arduino_a.write(command.encode()) 
  arduino_t.write(command.encode())

    
    
