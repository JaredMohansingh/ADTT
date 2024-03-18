import serial
import time

arduino_a = serial.Serial('/dev/ttyACM0', 9600) 
arduino_t = serial.Serial('/dev/ttyACM2', 9600) 
val_a = 89
val_t = 90
laser_on = "l"
laser_off = "n"
jnt = "000"
arduino_a.write(str(val_a).encode())
arduino_t.write(str(val_t).encode())
bias_a = 0
bias_t = 0
time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
    jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")
    
    if( jnt[0] == "l"):
        arduino_t.write(laser_on.encode()) 
    if( jnt[0] == "n"):
        arduino_t.write(laser_off.encode()) 

    if( jnt[0] == "a"):

        if (jnt[1] == "u"):
            val_a = val_a +1

        if (jnt[1] == "d"):
            val_a = val_a -1


        if (jnt[1] == "y"):
            val_a = val_a +10

        if (jnt[1] == "s"):
            val_a = val_a -10

        if (jnt[1] == "t"):
            val_a = val_a +50

        if (jnt[1] == "a"):
            val_a = val_a -50

        if (jnt[1:].isdigit()):
            val_a = float(jnt[1:])

        if ( jnt[1]== "b" ):
            bias_a = val_a
            val_a = 0 

        arduino_a.write(str(val_a + bias_a).encode()) 
        
    ################################################

    if( jnt[0] == "t"):

        if (jnt[1] == "u"):
            val_t = val_t +1

        if (jnt[1] == "d"):
            val_t = val_t -1


        if (jnt[1] == "y"):
            val_t = val_t +10

        if (jnt[1] == "s"):
            val_t = val_t -10

        if (jnt[1] == "t"):
            val_t = val_t +50

        if (jnt[1] == "a"):
            val_t = val_t -50


        if (jnt[1:].isdigit()):
            val_t = float(jnt[1:])

        if ( jnt[1]== "b" ):
            bias_t = val_t
            val_t = 0 

        arduino_t.write(str(val_t + bias_t ).encode()) 
        
    print("Val a is  ")
    print(val_a)
    print(" ")
    print("Val t is ")
    print(val_t)
    print(" ")
    
    
    

    
    

