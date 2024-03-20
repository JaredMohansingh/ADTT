import serial
import time

arduino_a = serial.Serial('/dev/ttyACM0', 9600) 
arduino_t = serial.Serial('/dev/ttyACM2', 9600) 
val_a = 0
val_t = 0
laser_on = "l"
laser_off = "n"
reset_sensor = "r"
jnt = "000"


time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
    jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")

    if( jnt[0] == "a"):

        if ( jnt[1]== "r" ):
            arduino_a.write(reset_sensor.encode())
            val_a = 0 

        if (jnt[1] == "u"):
            val_a = val_a +45
            arduino_a.write(str(val_a ).encode()) 
        
        if (jnt[1] == "d"):
            val_a = val_a -45
            arduino_a.write(str(val_a ).encode()) 
        
        if (jnt[1:].isdigit()):
            val_a = float(jnt[1:])
            arduino_a.write(str(val_a ).encode()) 
        
    ################################################

    if( jnt[0] == "l"):
        arduino_t.write(laser_on.encode()) 
    if( jnt[0] == "n"):
        arduino_t.write(laser_off.encode()) 

    if( jnt[0] == "t"):

        if ( jnt[1]== "r" ):
          arduino_t.write(reset_sensor.encode())
          val_t = 0 

        if (jnt[1] == "u"):
          val_t = val_t +45
          arduino_t.write(str(val_t ).encode()) 
      
        if (jnt[1] == "d"):
          val_t = val_t -45
          arduino_t.write(str(val_t ).encode()) 
      
        if (jnt[1:].isdigit()):
          val_t = float(jnt[1:])
          arduino_t.write(str(val_t ).encode()) 
      
    print("Val a is  ")
    print(val_a)
    print(" ")
    print("Val t is ")
    print(val_t)
    print(" ")
    
    
    

    
    

